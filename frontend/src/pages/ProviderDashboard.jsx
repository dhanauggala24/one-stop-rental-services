import Navbar from "../components/Navbar";

function ProviderDashboard() {
  return (
    <div>
      <Navbar />

      <div className="container mt-4">
        <div className="card shadow p-4">
          <h1>Provider Dashboard</h1>

          <p className="mt-3">
            Welcome Provider 🏪
          </p>

          <ul>
            <li>Create Item</li>
            <li>Manage My Items</li>
            <li>View Provider Bookings</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default ProviderDashboard;