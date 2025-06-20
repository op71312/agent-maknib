function dummyAI(board, difficulty, timeLeft, aiPieceId, moveHistory) {
  const size = board.length;
  const moves = [];

  for (let r = 0; r < size; r++) {
    for (let c = 0; c < size; c++) {
      if (board[r][c] === aiPieceId) {
        for (let cc = 0; cc < size; cc++) {
          if (cc !== c && board[r][cc] === 0 && clearPath(board, r, c, r, cc)) {
            moves.push({ from: [r, c], to: [r, cc] });
          }
        }
        for (let rr = 0; rr < size; rr++) {
          if (rr !== r && board[rr][c] === 0 && clearPath(board, r, c, rr, c)) {
            moves.push({ from: [r, c], to: [rr, c] });
          }
        }
      }
    }
  }

  const selected = moves[Math.floor(Math.random() * moves.length)] || {};
  const thoughts = `AI (ระดับ ${difficulty}) เลือกเดินจาก ${JSON.stringify(selected)} เพื่อควบคุมตำแหน่ง`;

  return {
    from: selected.from || null,
    to: selected.to || null,
    thoughts
  };
}

function clearPath(board, r1, c1, r2, c2) {
  if (r1 === r2) {
    const [start, end] = [Math.min(c1, c2), Math.max(c1, c2)];
    for (let i = start + 1; i < end; i++) {
      if (board[r1][i] !== 0) return false;
    }
  } else if (c1 === c2) {
    const [start, end] = [Math.min(r1, r2), Math.max(r1, r2)];
    for (let i = start + 1; i < end; i++) {
      if (board[i][c1] !== 0) return false;
    }
  } else return false;
  return true;
}

module.exports = {
  dummyAI
};
