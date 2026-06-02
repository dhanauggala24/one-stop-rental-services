import { useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar";

function UserDashboard() {
  const navigate = useNavigate();

  const categories = [
    {
      name: "Property Rental",
      icon: "🏠",
      description: "Houses, apartments, rooms, and rental properties",
    },
    {
      name: "PG & Hostel",
      icon: "🏢",
      description: "PGs, hostels, shared rooms, and student stays",
    },
    {
      name: "Vehicles",
      icon: "🚗",
      description: "Cars, bikes, scooters, and travel rentals",
    },
    {
      name: "Photography",
      icon: "📷",
      description: "Cameras, drones, lenses, and event gear",
    },
    {
      name: "Equipment",
      icon: "🔧",
      description: "Tools, machines, projectors, and rental equipment",
    },
    {
      name: "Camping",
      icon: "🏕️",
      description: "Tents, trekking kits, sleeping bags, and outdoor gear",
    },
  ];

  return (
    <div>
      <Navbar />

      <div className="container mt-4">
        <h1 className="mb-2">User Dashboard</h1>

        <p className="text-muted mb-4">
          Choose a rental category and find items near your location.
        </p>

        <div className="row">
          {categories.map((category) => (
            <div className="col-md-4 mb-4" key={category.name}>
              <div className="card shadow h-100 text-center p-4">
                <h1>{category.icon}</h1>

                <h4>{category.name}</h4>

                <p className="text-muted">{category.description}</p>

                <button
                  className="btn btn-primary mt-auto"
                  onClick={() =>
                    navigate(`/items?category=${encodeURIComponent(category.name)}`)
                  }
                >
                  View Items
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default UserDashboard;