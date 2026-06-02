import axios from "axios";

const API = axios.create({
  baseURL: "https://one-stop-rental-backend.onrender.com",
});

export default API;