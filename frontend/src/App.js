import logo from './logo.svg';
import './App.css';
import React, {useEffect, useState} from "react";

function App() {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        async function fetchMyAPI() {
            let response = await fetch('/api/users')
            response = await response.json()
            setUsers(response.results)
        }

        fetchMyAPI()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo"/>
                <h5>Users fetched from backend API (http://localhost:8000/api/users/):</h5>
                {users.map((user, index) =>
                    <li key={index}>{user.username} - {user.email} - {(user.url).replace("backend", "localhost")}</li>)}
                {console.log(users)}
            </header>
        </div>
    );
}

export default App;
