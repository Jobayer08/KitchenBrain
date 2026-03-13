import { useState, useEffect } from "react";

function App() {

const [name, setName] = useState("");
const [expiry, setExpiry] = useState("");
const [foods, setFoods] = useState([]);

// Add food
const addFood = async () => {

await fetch("http://127.0.0.1:5000/add_food", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    name: name,
    expiry: expiry
  })
});

alert("Food Added");

loadFoods();

};

// Load foods
const loadFoods = async () => {

const res = await fetch("http://127.0.0.1:5000/foods");

const data = await res.json();

setFoods(data);

};

// Delete food
const deleteFood = async (id) => {

await fetch(`http://127.0.0.1:5000/delete_food/${id}`, {
  method: "DELETE"
});

loadFoods();

};

// Expiry color logic
const getExpiryStatus = (expiryDate) => {

const today = new Date();
const expiry = new Date(expiryDate);

const diff = (expiry - today) / (1000 * 60 * 60 * 24);

if (diff < 0) {
  return "red";
}
else if (diff <= 2) {
  return "orange";
}
else {
  return "green";
}

};

// Check expiry alert
const checkExpiry = async () => {

const res = await fetch("http://127.0.0.1:5000/check_expiry");

const data = await res.json();

if (data.length > 0) {

  alert("⚠ Some food items are about to expire!");
  console.log(data);

}

};

// Page load
useEffect(() => {

loadFoods();

const interval = setInterval(() => {
  checkExpiry();
}, 10000);

return () => clearInterval(interval);

}, []);

return (
<div style={{ padding: "40px" }}>

  <h1>KitchenBrain</h1>

  <input
    placeholder="Food Name"
    onChange={(e) => setName(e.target.value)}
  />

  <br /><br />

  <input
    type="date"
    onChange={(e) => setExpiry(e.target.value)}
  />

  <br /><br />

  <button onClick={addFood}>
    Add Food
  </button>

  <br /><br />

  <h2>Fridge Inventory</h2>

  <table border="1" cellPadding="10">

    <tr>
      <th>Food</th>
      <th>Expiry</th>
      <th>Status</th>
      <th>Action</th>
    </tr>

    {foods.map((food) => {

      const color = getExpiryStatus(food.expiry);

      return (

        <tr key={food.id}>

          <td>{food.name}</td>

          <td>{food.expiry}</td>

          <td style={{ color: color }}>
            {color === "red" && "🔴 Expired"}
            {color === "orange" && "🟡 Expiring Soon"}
            {color === "green" && "🟢 Fresh"}
          </td>

          <td>
            <button onClick={() => deleteFood(food.id)}>
              Delete
            </button>
          </td>

        </tr>

      );

    })}

  </table>

</div>

);
}

export default App;