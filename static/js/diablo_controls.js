let arrowKeysPressed = {
    // ArrowUp: false,
    // ArrowDown: false,
    // ArrowLeft: false,
    // ArrowRight: false
  };
// API = 'https://vaibhav25001.pythonanywhere.com'
API = 'http://10.241.144.104:5000'
  window.addEventListener('keydown', function(event) {
    if (event.key === 'w' || event.key === 's' || event.key === 'a' || event.key === 'd' || event.key === 'z' || event.key === 'x' || event.key === 'q' || event.key === 'e' || event.key === 'c' || event.key === 'o' || event.key === 'Space' || event.code == 32 || event.key === ' ' ) {
      arrowKeysPressed[event.key] = true;
      if (event.key === 'w') {
        sendToAPI("1");
      } else if (event.key === 's'){
        sendToAPI("2");
      } else if (event.key === 'a'){
        sendToAPI("3");
      } else if (event.key === 'd'){
        sendToAPI("4");
      } else if (event.key === 'z'){
        sendToAPI("5")
      } else if (event.key === 'x'){
        sendToAPI("6")
      } else if (event.key === 'q'){
        sendToAPI("7")
      } else if (event.key === 'e'){
        sendToAPI("8")
      } else if (event.key === 'c'){
        sendToAPI("9")
      } else if (event.key === 'o'){
        sendToAPI("0")
      } else if (event.key === 'Space'){
        sendToAPI("0")
      } else if (event.code === 32){
        sendToAPI("0")
      } else if (event.key === ' '){
        sendToAPI("0")
      }
      checkArrowKeysPressed();
    }
  });

  window.addEventListener('keyup', function(event) {
    if (event.key === 'w' || event.key === 's' || event.key === 'a' || event.key === 'd' || event.key === 'z' || event.key === 'x' || event.key === 'q' || event.key === 'e' || event.key === 'c' || event.key === 'o' || event.key === 'Space' || event.code == 32 || event.key === ' ') {
      arrowKeysPressed[event.key] = false;
      if (event.key === 'w' || event.key === 's' || event.key === 'a' || event.key === 'd' || event.key === 'z' || event.key === 'x' || event.key === 'q' || event.key === 'e' || event.key === 'c' || event.key === 'o' || event.key === 'Space' || event.code == 32 || event.key === ' ') {
        updateDataValue0();
      }
      checkArrowKeysPressed();
      
    }
  });

  function sendToAPI(Vdata) {
    const apiUrl = API + '/api/update_data_post'; // Replace with your API endpoint
    fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ key: 'data', new_value: Vdata })
    })
      .then(response => {
        if (response.ok) {
          console.log(`Successfully updated data to ${Vdata}`);
        } else {
          console.log(`Failed to update data`);
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }
  function updateDataValue0() {
    const apiUrl = API + '/api/update_data_post'; // Replace with your API endpoint
    fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ key: 'data', new_value: "0" })
    })
      .then(response => {
        if (response.ok) {
          console.log(`Successfully updated data to 0`);
        } else {
          console.log(`Failed to update data`);
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }

  function checkArrowKeysPressed() {
    console.clear(); // Clear console for easier readability

    Object.keys(arrowKeysPressed).forEach(function(key) {
      if (arrowKeysPressed[key]) {
        console.log(`${key} is pressed`);
      } else {
        console.log(`${key} is not pressed`);
      }
    });
  }

  setInterval(() => {
    updateDataValue0()
  }, 500);