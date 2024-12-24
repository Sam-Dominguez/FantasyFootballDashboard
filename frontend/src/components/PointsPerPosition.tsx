import React, { useEffect, useState } from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { Spinner } from "react-bootstrap";
import axios from 'axios';
import { useTeamContext } from './TeamContext.tsx'; // Import your context

function PointsPerPosition() {
  const [data, setData] = useState([{}]);
  const [loading, setLoading] = useState(true);

  // Get the selected team id from the context
  const { selectedTeamId } = useTeamContext();

   // Log the selected teamId to check if it's being updated
   console.log('Selected Team ID:', selectedTeamId);

  useEffect(() => {
    // Fetch data only when selectedTeamId changes (or on initial render)
    const fetchData = async () => {
      if (selectedTeamId === "__") {
        console.log('No team selected, skipping API call');
        setLoading(false);
        return; // Don't fetch data if no team is selected
      }
        
      setLoading(true); // Start loading
      console.log('Fetching data for team ID:', selectedTeamId); // Log API call

      try {
        // Make an API call using the selected team id
        const response = await axios.get(`http://127.0.0.1:8000/points_per_position/${selectedTeamId}`);
        setData(Object.keys(response.data).map(week => ({
          week: `Week ${week}`,
          ...response.data[week]
        })));
        setLoading(false); // Data fetched, stop loading
      } catch (error) {
        console.error("Error fetching data:", error);
        setLoading(false); // Stop loading even in case of error
      }
    };

    fetchData(); // Fetch the data on initial load or when selectedTeamId changes
  }, [selectedTeamId]); // Effect runs whenever selectedTeamId changes

  return (
    <div className="container-fluid vh-100 d-flex justify-content-center align-items-center bg-light">
      {loading ? (
        // Show Spinner while loading
        <Spinner animation="border" role="status" className="text-primary">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
      ) : (
        // Show Chart when data is ready
        <div className="col-12 col-md-10 col-lg-8">
          <ResponsiveContainer width="100%" height={600}>
            <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="week" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="WR" stroke="#8884d8" />
              <Line type="monotone" dataKey="RB" stroke="#82ca9d" />
              <Line type="monotone" dataKey="TE" stroke="#ff7300" />
              <Line type="monotone" dataKey="QB" stroke="#387908" />
              <Line type="monotone" dataKey="D" stroke="#888888" />
              <Line type="monotone" dataKey="K" stroke="#ff1493" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
};

export default PointsPerPosition;
