import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import math

# ====== ENVIRONMENT CLASS ======
class MakNeebRLEnv:
    def __init__(self):
        self.board_size = 8
        self.action_space_n = self.board_size ** 4
        self.reset()

    def reset(self, board=None, current_player=1):
        if board is not None:
            self.board = np.array(board, dtype=np.int8)
        else:
            self.board = np.zeros((self.board_size, self.board_size), dtype=np.int8)
            self.board[0, :] = 1
            self.board[7, :] = -1
        self.current_player = current_player
        self.turns_without_capture = 0
        self.max_turns_without_capture = 50
        return self.board.copy(), {"current_player": self.current_player}

    def _encode_action(self, from_row, from_col, to_row, to_col):
        return from_row * (8*8*8) + from_col * (8*8) + to_row * 8 + to_col

    def _decode_action(self, action):
        from_row = action // (8*8*8)
        action %= (8*8*8)
        from_col = action // (8*8)
        action %= (8*8)
        to_row = action // 8
        to_col = action % 8
        return (from_row, from_col), (to_row, to_col)

    def get_legal_actions(self):
        legal_actions = []
        for r_from in range(self.board_size):
            for c_from in range(self.board_size):
                if self.board[r_from, c_from] == self.current_player:
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        for i in range(1, self.board_size):
                            r_to, c_to = r_from + dr * i, c_from + dc * i
                            if not (0 <= r_to < self.board_size and 0 <= c_to < self.board_size):
                                break
                            if self.board[r_to, c_to] != 0:
                                break
                            action = self._encode_action(r_from, c_from, r_to, c_to)
                            legal_actions.append(action)
        return legal_actions

    def step(self, action):
        legal_actions = self.get_legal_actions()
        if action not in legal_actions:
            return self.board.copy(), -10.0, True, False, {"error": "Illegal move"}
        (from_row, from_col), (to_row, to_col) = self._decode_action(action)
        self.board[to_row, to_col] = self.current_player
        self.board[from_row, from_col] = 0
        captured_count = self._check_and_capture(to_row, to_col)
        reward = captured_count * 2
        if captured_count > 0:
            self.turns_without_capture = 0
        else:
            self.turns_without_capture += 1
        done, winner = self.get_game_status()
        if done:
            if winner == self.current_player:
                reward += 20
            elif winner == -self.current_player:
                reward -= 20
            elif winner == 0:
                reward += 5
        self.current_player *= -1
        info = {"current_player": self.current_player, "captured": captured_count > 0}
        return self.board.copy(), float(reward), done, False, info

    def _check_and_capture(self, row, col):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        captured = set()
        my = self.current_player
        enemy = -self.current_player

        for dr, dc in directions:
            # Pattern 1: Classic sandwich capture
            to_capture = []
            r, c = row + dr, col + dc
            # Traverse in direction while enemies are found
            while self._in_bounds(r, c) and self.board[r][c] == enemy:
                to_capture.append((r, c))
                r += dr
                c += dc
            # Capture if enemies are sandwiched by boundary or own piece
            if to_capture:
                if not self._in_bounds(r, c) or self.board[r][c] == my:
                    captured.update(to_capture)
            # Pattern 2: Immediate adjacent capture
            adj_r1, adj_c1 = row - dr, col - dc
            adj_r2, adj_c2 = row + dr, col + dc
            if (self._in_bounds(adj_r1, adj_c1) and 
                self._in_bounds(adj_r2, adj_c2) and
                self.board[adj_r1][adj_c1] == enemy and
                self.board[adj_r2][adj_c2] == enemy):
                captured.add((adj_r1, adj_c1))
                captured.add((adj_r2, adj_c2))
        # Remove captured pieces
        for r, c in captured:
            self.board[r][c] = 0
        return len(captured)

    def get_game_status(self):
        player1_pieces = np.sum(self.board == 1)
        player_minus_1_pieces = np.sum(self.board == -1)
        if player1_pieces == 0:
            return True, -1
        if player_minus_1_pieces == 0:
            return True, 1
        if not self.get_legal_actions_for_player(-self.current_player):
            return True, self.current_player
        if self.turns_without_capture >= self.max_turns_without_capture:
            if player1_pieces > player_minus_1_pieces:
                return True, 1
            elif player_minus_1_pieces > player1_pieces:
                return True, -1
            else:
                return True, 0
        return False, 0

    def get_legal_actions_for_player(self, player):
        for r_from in range(self.board_size):
            for c_from in range(self.board_size):
                if self.board[r_from, c_from] == player:
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        r_to, c_to = r_from + dr, c_from + dc
                        if (0 <= r_to < self.board_size and
                            0 <= c_to < self.board_size and
                            self.board[r_to, c_to] == 0):
                            return [1]
        return []

    def render(self, mode='human'):
        pass

    def copy(self):
        new_env = MakNeebRLEnv()
        new_env.board = self.board.copy()
        new_env.current_player = self.current_player
        new_env.turns_without_capture = self.turns_without_capture
        return new_env

    def _in_bounds(self, r, c):
        return 0 <= r < self.board_size and 0 <= c < self.board_size

# ====== MODEL ======
class ResNetBlock(nn.Module):
    def __init__(self, num_channels):
        super().__init__()
        self.conv1 = nn.Conv2d(num_channels, num_channels, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(num_channels)
        self.conv2 = nn.Conv2d(num_channels, num_channels, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(num_channels)
    def forward(self, x):
        residual = x
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += residual
        return F.relu(out)

class MakNeebNet(nn.Module):
    def __init__(self, board_size=8, num_res_blocks=5, num_channels=64, action_size=4096):
        super().__init__()
        self.conv_in = nn.Conv2d(1, num_channels, kernel_size=3, padding=1)
        self.bn_in = nn.BatchNorm2d(num_channels)
        self.res_blocks = nn.ModuleList([ResNetBlock(num_channels) for _ in range(num_res_blocks)])
        self.policy_conv = nn.Conv2d(num_channels, 2, kernel_size=1)
        self.policy_bn = nn.BatchNorm2d(2)
        self.policy_fc = nn.Linear(2 * board_size * board_size, action_size)
        self.value_conv = nn.Conv2d(num_channels, 1, kernel_size=1)
        self.value_bn = nn.BatchNorm1d(1 * board_size * board_size)
        self.value_fc1 = nn.Linear(1 * board_size * board_size, 256)
        self.value_fc2 = nn.Linear(256, 1)
    def forward(self, x):
        x = x.unsqueeze(1)
        x = F.relu(self.bn_in(self.conv_in(x)))
        for block in self.res_blocks:
            x = block(x)
        policy = F.relu(self.policy_bn(self.policy_conv(x)))
        policy = policy.view(policy.size(0), -1)
        policy = self.policy_fc(policy)
        value = F.relu(self.value_conv(x))
        value = value.view(value.size(0), -1)
        value = self.value_bn(value)
        value = F.relu(self.value_fc1(value))
        value = torch.tanh(self.value_fc2(value))
        return F.log_softmax(policy, dim=1), value

# ====== MCTS (Minimal for 1 move) ======
class MCTSNode:
    def __init__(self, parent=None, prior_p=1.0):
        self.parent = parent
        self.children = {}
        self.visit_count = 0
        self.value_sum = 0
        self.prior_p = prior_p
    def expand(self, action_priors):
        for action, prior in action_priors:
            if action not in self.children:
                self.children[action] = MCTSNode(parent=self, prior_p=prior)
    def select(self, c_puct):
        best_score = -float('inf')
        best_action = -1
        best_child = None
        for action, child in self.children.items():
            score = self.get_ucb_score(child, c_puct)
            if score > best_score:
                best_score, best_action, best_child = score, action, child
        return best_action, best_child
    def get_ucb_score(self, child, c_puct):
        q_value = child.value()
        u_value = c_puct * child.prior_p * math.sqrt(self.visit_count) / (1 + child.visit_count)
        return q_value + u_value
    def value(self):
        return self.value_sum / self.visit_count if self.visit_count > 0 else 0
    def backpropagate(self, value):
        self.visit_count += 1
        self.value_sum += value
        if self.parent:
            self.parent.backpropagate(-value)

class MCTS:
    def __init__(self, model, device, c_puct=1.5, num_simulations=100):
        self.model = model
        self.device = device
        self.c_puct = c_puct
        self.num_simulations = num_simulations
    @torch.no_grad()
    def search(self, env):
        root = MCTSNode()
        initial_board_tensor = torch.tensor(
            env.board * env.current_player,
            dtype=torch.float32
        ).unsqueeze(0).to(self.device)
        log_policy, value = self.model(initial_board_tensor)
        policy = torch.exp(log_policy).squeeze(0).cpu().numpy()
        legal_actions = env.get_legal_actions()
        if not legal_actions:
            return np.ones(env.action_space_n) / env.action_space_n, value.item()
        action_priors = [(action, policy[action]) for action in legal_actions]
        root.expand(action_priors)
        for _ in range(self.num_simulations):
            node = root
            sim_env = MakNeebRLEnv()
            sim_env.board = env.board.copy()
            sim_env.current_player = env.current_player
            sim_env.turns_without_capture = env.turns_without_capture
            # Selection
            while node is not None and getattr(node, "children", None):
                action, next_node = node.select(self.c_puct)
                if next_node is None:
                    break
                node = next_node
                sim_env.step(action)
            # Evaluation
            done, winner = sim_env.get_game_status()
            value = 0
            if not done:
                board_tensor = torch.tensor(
                    sim_env.board * sim_env.current_player,
                    dtype=torch.float32
                ).unsqueeze(0).to(self.device)
                log_policy, value_tensor = self.model(board_tensor)
                policy = torch.exp(log_policy).squeeze(0).cpu().numpy()
                value = value_tensor.item()
                legal_actions = sim_env.get_legal_actions()
                if legal_actions:
                    action_priors = [(action, policy[action]) for action in legal_actions]
                    node.expand(action_priors)
            else:
                if winner != 0:
                    value = 1 if winner == sim_env.current_player else -1
            node.backpropagate(-value)
        visit_counts = np.array([
            root.children.get(a, MCTSNode()).visit_count
            for a in range(env.action_space_n)
        ])
        if visit_counts.sum() == 0:
            return np.ones(env.action_space_n) / env.action_space_n, root.value()
        action_probs = visit_counts / visit_counts.sum()
        return action_probs, root.value() 