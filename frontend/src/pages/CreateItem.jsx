import { useState } from "react";
import API from "../api/axios";
import Navbar from "../components/Navbar";

function CreateItem() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [pricePerDay, setPricePerDay] = useState("");
  const [location, setLocation] = useState("");
  const [category, setCategory] = useState("Property Rental");

  const handleCreateItem = async () => {
    try {
      const token = localStorage.getItem("token");

      const response = await API.post(
        "/create-item",
        {
          title,
          description,
          price_per_day: Number(pricePerDay),
          location,
          category,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      alert(response.data.message);

      setTitle("");
      setDescription("");
      setPricePerDay("");
      setLocation("");
      setCategory("Property Rental");
    } catch (error) {
      console.log(error.response?.data || error.message);
      alert("Failed to create item");
    }
  };

  return (
    <div>
      <Navbar />

      <div className="container mt-4">
        <div className="card shadow p-4">
          <h1 className="mb-4">Create Rental Item</h1>

          <input
            type="text"
            className="form-control mb-3"
            placeholder="Item Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />

          <input
            type="text"
            className="form-control mb-3"
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />

          <input
            type="number"
            className="form-control mb-3"
            placeholder="Price Per Day"
            value={pricePerDay}
            onChange={(e) => setPricePerDay(e.target.value)}
          />

          <input
            type="text"
            className="form-control mb-3"
            placeholder="Location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />

          <select
            className="form-select mb-3"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          >
            <option value="Property Rental">Property Rental</option>
            <option value="Vehicles">Vehicles</option>
            <option value="Photography">Photography</option>
            <option value="Equipment">Equipment</option>
            <option value="Camping">Camping</option>
          </select>

          <button
            className="btn btn-primary"
            onClick={handleCreateItem}
          >
            Create Item
          </button>
        </div>
      </div>
    </div>
  );
}

export default CreateItem;