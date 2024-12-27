import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Spinner } from 'react-bootstrap';
import { Bar, BarChart, CartesianGrid, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

function PointsOnBench() {

    const [data, setData] = useState([{}]);
    const [loading, setLoading] = useState(false)
    const [average, setAverage] = useState(0)


    useEffect(() => {
        const fetchData = async () => {
            setLoading(true); // Start loading

            try {
                const response = await axios.get(`http://127.0.0.1:8000/points_on_bench`);
                const response_data = Object.entries(response.data.teams)
                    .map(([teamNumber, value]) => ({
                        team: `Team ${teamNumber}`,
                        points: value as number
                    }));

                response_data.sort((a, b) => b.points - a.points)

                setAverage(response.data.average)
                setData(response_data);
                setLoading(false);
            } catch (error) {
                console.error("Error fetching data:", error);
                setLoading(false);
            }
        };

        fetchData(); // Fetch the data on initial load or when selectedTeamId changes
    }, [setLoading]); // Effect runs whenever selectedTeamId changes

    return (
        <div className="container-fluid vh-100 d-flex flex-column justify-content-center align-items-center">
            <h3 className="text-center mb-4">
                Points Left on Bench
            </h3>
            {loading ? (
                // Show Spinner while loading
                <Spinner animation="border" role="status" className="text-primary">
                    <span className="visually-hidden">Loading...</span>
                </Spinner>
            ) : (
                // Show Chart when data is ready
                <div className="col-12 col-md-10 col-lg-8">
                    <ResponsiveContainer width="100%" height={600}>
                        <BarChart
                            width={2000}
                            height={400}
                            data={data}
                            margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                        >
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="team" />
                            <YAxis domain={[0, 1000]} />
                            <Tooltip />
                            <Bar dataKey="points" fill="#4f46e5" />
                            <ReferenceLine y={average} stroke="#ef4444" strokeDasharray="3 3" label="Average" />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            )}
        </div>
    );
};

export default PointsOnBench;
