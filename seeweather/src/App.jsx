import React, { useState, useEffect } from 'react';
import './index.css'; // Ensure your Tailwind CSS is imported here

export default function App() {
  const [city, setCity] = useState('');
  const [weather, setWeather] = useState(null);

  const search = async (city) => {
    try {
      const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${import.meta.env.VITE_APP_KEY}`;
      const response = await fetch(url);
      const data = await response.json();
      if (response.ok) {
        setWeather(data);
        console.log(data);
      } else {
        console.error('Error fetching weather data:', data.message);
      }
    } catch (error) {
      console.error('Network error:', error);
    }
  };

  const handleSearch = (event) => {
    if (event.key === 'Enter' && city.trim() !== '') {
      search(city);
    }
  };


  return (
    <div className="bg-gradient-to-br from-blue-400 to-blue-600 min-h-screen flex flex-col items-center justify-center text-white p-4">
      <h1 className="text-3xl font-bold mb-4">Weather</h1>
      <input
        type="search"
        className="w-full max-w-md p-2 text-black rounded-md shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        value={city}
        onChange={(e) => setCity(e.target.value)}
        onKeyDown={handleSearch}
        placeholder="Enter city name"
      />
      {weather && (
        <div className="mt-6 p-4 bg-white bg-opacity-20 rounded-lg shadow-md text-center w-full max-w-md">
          <h2 className="text-2xl font-semibold">{weather.name}</h2>
          <p className="text-lg">{weather.weather[0].description}</p>
          <p className="text-4xl font-bold mt-2">
            {(weather.main.temp - 273.15).toFixed(2)}°C
          </p>
        </div>
      )}
    </div>
  );
}
