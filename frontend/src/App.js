import { useState } from "react";

function App() {

  const [name,setName]=useState("")
  const [expiry,setExpiry]=useState("")

  const addFood = async () => {

    await fetch("http://127.0.0.1:5000/add_food",{
      method:"POST",
      headers:{
        "Content-Type":"application/json"
      },
      body:JSON.stringify({
        name:name,
        expiry:expiry
      })
    })

    alert("Food Added")
  }

  return (
    <div style={{padding:"40px"}}>
      <h1>KitchenBrain</h1>

      <input placeholder="Food Name"
      onChange={(e)=>setName(e.target.value)} />

      <br/><br/>

      <input type="date"
      onChange={(e)=>setExpiry(e.target.value)} />

      <br/><br/>

      <button onClick={addFood}>
        Add Food
      </button>

    </div>
  );
}

export default App;