// public/config.js

const BACKEND_LOCAL = "http://localhost:8000";
const BACKEND_RENDER = "https://blood-flow-backend.onrender.com";

export const API_BASE =
    location.hostname === "localhost"
        ? BACKEND_LOCAL
        : BACKEND_RENDER;
