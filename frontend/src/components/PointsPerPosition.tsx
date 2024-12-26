import React, { useEffect, useState } from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { Spinner } from "react-bootstrap";
import axios from 'axios';
import { useTeamContext } from './TeamContext.tsx'; // Import your context
import { useLocation } from 'react-router-dom';

function PointsPerPosition() {
  const [data, setData] = useState([{}]);

  // Get the selected team id and name from the context
  const { selectedTeamId, loading, setLoading, setSelectedTeamId, selectedTeamName, setSelectedTeamName } = useTeamContext();
  const location = useLocation(); // To track the location

  // Reset team to "Whole League" when the page is navigated to
  useEffect(() => {
    if (location.pathname === '/points-per-position') {
      setSelectedTeamId("__"); // Reset to "Whole League"
      setSelectedTeamName("")
    }
  }, [location.pathname, setSelectedTeamId, setSelectedTeamName]); // Run on location change

  useEffect(() => {
    const fetchData = async () => {
      if (selectedTeamId === "__") {
        setLoading(false);
        return; // Don't fetch data if no team is selected
      }

      setLoading(true); // Start loading

      try {
        const response = await axios.get(`http://127.0.0.1:8000/points_per_position/${selectedTeamId}`);
        setData(Object.keys(response.data).map(week => ({
          week: `Week ${week}`,
          ...response.data[week]
        })));
        setLoading(false);
      } catch (error) {
        console.error("Error fetching data:", error);
        setLoading(false);
      }
    };

    fetchData(); // Fetch the data on initial load or when selectedTeamId changes
  }, [selectedTeamId, setLoading]); // Effect runs whenever selectedTeamId changes

  return (
    <div className="container-fluid vh-100 d-flex flex-column justify-content-center align-items-center">
      <h3 className="text-center mb-4">
        Point Breakdown per Position {selectedTeamName && `for ${selectedTeamName}`}
      </h3>
      {selectedTeamId === "__" ? (
        // Show prompt to select a team
        <h5 className="text-muted">Please select a team to view the chart.</h5>
      ) : loading ? (
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
              <YAxis domain={['dataMin', 'dataMax']}/>
              <Tooltip
                itemSorter={(item) => {
                  return (item.value as number) * -1;
                }}
              />
              <Legend />
              <Line type="monotone" dataKey="WR" stroke="#8884d8" />
              <Line type="monotone" dataKey="RB" stroke="#82ca9d" />
              <Line type="monotone" dataKey="TE" stroke="#ff7300" />
              <Line type="monotone" dataKey="QB" stroke="#387908" />
              <Line type="monotone" dataKey="D/ST" stroke="#888888" />
              <Line type="monotone" dataKey="K" stroke="#ff1493" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
};

export default PointsPerPosition;
