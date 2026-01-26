function toDay() {
  var date = new Date();
  var day = date.getDate();
  var month = date.getMonth() + 1;
  var year = date.getFullYear();
  // Sử dụng phương thức padStart để thêm '0' tiện lợi hơn (ES6)
  var formattedMonth = String(month).padStart(2, "0");
  var formattedDay = String(day).padStart(2, "0");
  // Định dạng YYYY-MM-DD
  return year + "-" + formattedMonth + "-" + formattedDay;
}

function changeDateFormat(val) {
  const myArray = val.split("-");

  let year = myArray[0];
  let month = myArray[1];
  let day = myArray[2];

  return day + "/" + month + "/" + year;
}
