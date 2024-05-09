// Commentary by Jabulani Lubisi
//This is the input validating function, it takes user input temperature and validates if it's a number or not
//First the input variables is declared and an event listener attached...
//This is a function that waits for a specific event to occur "Keypress" and then executes a designated action in response,
//in this case if the input is not a number it alerts the string "That wa not a valid number"

let Input = document.getElementById("Inputtemperature");
    Input.addEventListener("keypress", function() {
        if (isNaN(this.value + String.fromCharCode(event.keyCode))) {
            alert("That was not a valid number,please enter a valid input then select appropriate unit from drop down menu");
            return false;
        }
    }); 

// THE main convert-temperature function is defined:
function convertTemperature() {
  // Get the input value and the selected units
  //The input value, fromUnit and toUnit are declared as a constants as fetched from the user input(1)(2)(3)
  const inputValue = parseFloat(document.getElementById("Inputtemperature").value);
 //Temperature input is parsed("%"-string) to extract numeric values from it i.e the user input string
  const fromUnit = document.getElementById("FromTemperatureUnit").value;
  const toUnit = document.getElementById("ToTemperatureUnit").value;

  // Performing the conversion:
  //First the result variables is declared under specified conditions i.e the FromUnit &ToUnit
  //Formulation to acquire result given
  //else statement lists the alternative blocks of code to execute if the initial condition i.e in the if statement is not true/like otherwise.
  let result;

  if (fromUnit === "celsius" && toUnit === "fahrenheit") {
      result = (inputValue * 9/5) + 32;
  } else if (fromUnit === "celsius" && toUnit === "kelvin") {
      result = inputValue + 273.15;
  } else if (fromUnit === "fahrenheit" && toUnit === "celsius") {
      result = (inputValue - 32) * 5/9;
  } else if (fromUnit === "fahrenheit" && toUnit === "kelvin") {
      result = (inputValue - 32) * 5/9 + 273.15;
  } else if (fromUnit === "kelvin" && toUnit === "celsius") {
      result = inputValue - 273.15;
  } else if (fromUnit === "kelvin" && toUnit === "fahrenheit") {
      result = (inputValue - 273.15) * 9/5 + 32;
  } else {
      result = inputValue;
      //Here we include one special condition, a conversion from celcius to celcis if To unit unspecified
  }

  // Displaying the result
  document.getElementById("temperatureResult").textContent = `Result: ${result.toFixed(2)} ${toUnit}`;
  //toUnit is used to give answer to two decimal places
  
};

