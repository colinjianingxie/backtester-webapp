function parseStringArray(stringArr){
  stringArr = stringArr.replace(/'/g, '"');
  return JSON.parse(stringArr)
}
