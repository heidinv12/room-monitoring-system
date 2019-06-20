import '../sass/styles.sass'

import { getJSON, postJSON } from './home'

const setContent = (id, content) => {
  const contentWrapper = document.getElementById(id)
  contentWrapper.defaultValue = content
}

const getContent = (id) => {
  const contentWrapper = document.getElementById(id)
  return contentWrapper.value
}

const deletePhone = (value) => {
	const body = {
		phone: value,
	}
	postJSON('DELETE_PHONE_ENDPOINT_URL', body)
}

const generateObjectList = (list, title) => {
  var table = document.createElement("table")
  var tblBody = document.createElement("tbody");
  list.forEach(listItem => {
  	const row = document.createElement("tr")
  	Object.keys(listItem).forEach(key => {
  		row.innerHTML += `<th>${listItem[key]}</th>`
  	})
    var head = document.createElement("th")
	row.appendChild(head)
	tblBody.appendChild(row); 
  })
  table.appendChild(tblBody)
  document.body.innerHTML += `<h4>${title}</h4>`
  document.body.appendChild(table)
}

const generateTableFromList = (list, title) => {
  var table = document.createElement("table")
  var tblBody = document.createElement("tbody");
  const shortList = list.length > 5 ? list.reverse().slice(0,5) : list.reverse()
  shortList.forEach(listItem => {
  	const row = document.createElement("tr")
  	row.innerHTML = `
	    <th>${listItem}</th>
  	`
	 tblBody.appendChild(row); 
  })
  table.appendChild(tblBody)
  document.body.innerHTML += `<h4>${title}</h4>`
  document.body.appendChild(table)
}

const generateRoomTempAndHum = (mintemp, maxtemp, minhum, maxhum, title) => {
  var table = document.createElement("table")
  var tblBody = document.createElement("tbody");
	const row = document.createElement("tr")
	row.innerHTML = `
    <th><p>Temperature (C)</p>Min: ${mintemp} | Max: ${maxtemp}</th>
    <th><p>Humidity (%)</p>Min: ${minhum} | Max: ${maxhum}</th>
	`
 tblBody.appendChild(row);
  table.appendChild(tblBody)
  document.body.innerHTML += `<h4>${title}</h4>`
  document.body.appendChild(table)
}

const generateRoomStatus = (temp, hum, title) => {
  var table = document.createElement("table")
  var tblBody = document.createElement("tbody");
	const row = document.createElement("tr")
	row.innerHTML = `
    <th><p>Temperature (C)</p>${temp}</th>
    <th><p>Humidity (%)</p>${hum}</th>
	`
 tblBody.appendChild(row);
  table.appendChild(tblBody)
  document.body.innerHTML += `<h4>${title}</h4>`
  document.body.appendChild(table)
}

const getConfig = (data) => {
	console.log(data.Configurations)
	console.log(data.Phones)
	console.log(data.Phones[0])
	const latest = data.Configurations
	setContent('humid', latest.Humidity)
	setContent('temp', latest.Temperature)
}

const submitContent = () => {
	console.log("submit content")
	const body = {
		minHumidity: getContent('minhumid'),
		maxHumidity: getContent('maxhumid'),
		minTemperature: getContent('mintemp'),
		maxTemperature: getContent('maxtemp'),
	}
	postJSON('CREATE_CONFIG_DATA_ENDPOINT_URL', body)
}

const submitPhoneContent = () => {
	const body = {
		user: getContent('user'),
		phone: getContent('phone'),
	}
	postJSON('CREATE_PHONE_DATA_ENDPOINT_URL', body)
}

getJSON('GET_DATA_ENDPOINT_URL').then(
      response => response.json().then(function(data) {
      	generateObjectList(data.Phones, 'Registered Phones');
      	generateRoomTempAndHum(data.Configurations.MinTemperature,
      	data.Configurations.MaxTemperature, data.Configurations.MinHumidity,
      	data.Configurations.MaxHumidity, 'Configuration Thresholds');
        generateRoomStatus(data.RoomTemperature, data.RoomHumidity, 'Actual Room Status');
        generateTableFromList(data.SmokeAlert, 'Smoke Sensor Triggered');
        generateTableFromList(data.MotionSensor, 'Motion Sensor Triggered');
        generateTableFromList(data.DoorSensor, 'Door Sensor Triggered');
		document.getElementById('button').onclick = () => submitContent()
		document.getElementById('phonebutton').onclick = () => submitPhoneContent()
      })
    ).catch(
      error => console.log(error)
    )
