import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useTeamContext } from './TeamContext.tsx';

function Header() {
    const [teams, setTeams] = useState<string[]>([]);

    const { setSelectedTeamId, loading, setSelectedTeamName } = useTeamContext();

    useEffect(() => {
        const fetchTeams = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:8000/teams");
                setTeams(response.data);
            } catch (error) {
                console.error("Error fetching teams:", error);
            }
        };

        fetchTeams();
    }, []);

    const navigate = useNavigate();
    const location = useLocation();

    const handleClick = () => {
        navigate('/');
    };

    const handleTeamChange = (event) => {
        setSelectedTeamId(event.target.value); // Update the selected team_id in context
        setSelectedTeamName(teams[event.target.value]);
    };

    // Define the routes where the select element should appear
    const showSelectOnRoutes = ['/points-per-position'];

    return (
        <div className='row sticky-top bg-white'>
            <div className='col-4'>
                <h2 onClick={handleClick} style={{ cursor: 'pointer' }}>Fantasy Football Dashboard</h2>
            </div>
            <div className='col-4' />
            <div className='col-4'>
                {showSelectOnRoutes.includes(location.pathname) && (
                    <select className="form-select" onChange={handleTeamChange} disabled={loading}>
                        <option value="__" selected>
                            - Whole League -
                        </option>
                        <optgroup label='Owned Teams'>
                            {Object.entries(teams).map(([id, name]) => (
                                <option key={id} value={id}>
                                    {name}
                                </option>
                            ))}
                        </optgroup>
                    </select>
                )}
            </div>
        </div>
    );
}

export default Header;
