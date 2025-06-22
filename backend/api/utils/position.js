const cols = ['a','b','c','d','e','f','g','h'];

function indexToPosition(row, col) {
  return `${cols[col]}${8 - row}`;
}

function positionToIndex(pos) {
  const col = cols.indexOf(pos[0].toLowerCase());
  const row = 8 - parseInt(pos[1], 10);
  return [row, col];
}

module.exports = {
  indexToPosition,
  positionToIndex
};
