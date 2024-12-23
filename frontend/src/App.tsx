import React, { useEffect, useState } from 'react';
import './App.css';
import axios from "axios"

function App() {

  const [item, setItem] = useState<string>();

   // Fetch items from the backend
   useEffect(() => {
    const fetchItems = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/");
        console.log(JSON.stringify(response))
        setItem(JSON.stringify(response.data));
      } catch (error) {
        console.error("Error fetching items:", error);
      }
    };

    fetchItems();
  }, []);
  

  return (
    <div className="App">
      <header className="App-header">
        <p>{item}</p>
      </header>
    </div>
  );
}

export default App;
