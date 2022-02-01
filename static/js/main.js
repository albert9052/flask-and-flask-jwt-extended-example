function login() {
	let data = {
		username: "test", 
		password: "test", 
	};
	fetch("./login", {
		method: "POST", 
		body: JSON.stringify(data),
		headers: {
			"content-type": "application/json"
		}
	}).then(res => res.json())
		.catch(error => console.error("Error", error))
		.then(response => console.log("Success", response));
}

function logout() {
	fetch("./logout", {
		method: "POST"
	}).then(res => res.json())
		.catch(error => console.error("Error", error))
		.then(response => console.log("Success", response));
}

function protected() {
	fetch("./protected", {
	}).then(res => res.json())
		.catch(error => console.error("Error", error))
		.then(response => console.log("Success", response));
}

function moreProtected() {
	fetch("./protected", {
	}).then(res => res.json())
		.catch(error => console.error("Error", error))
		.then(response => console.log("Success", response));
}
