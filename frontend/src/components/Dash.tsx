import React from 'react';
import { Link } from 'react-router-dom';

function Dash() {

  return (
    <div className='container'>
        <div className='row'>
            <div className='col'>
                    <div className="card">
                        <div className="card-body">
                            <h5 className="card-title">Points per Position Group</h5>
                            <p className="card-text">Breakdown of point contributions per position group to identify main sources of point production.</p>
                            <Link to="/points-per-position" className="btn btn-primary">Open</Link>
                        </div>
                    </div>
            </div>

            <div className='col'>
                    <div className="card">
                        <div className="card-body">
                            <h5 className="card-title">Average Draft Position vs Production</h5>
                            <p className="card-text">Comparison of ADP versus Point Production.</p>
                        <a href="#" className="btn btn-primary">Go somewhere</a>
                        </div>
                    </div>
            </div>
        </div>
    </div>
  );
}

export default Dash;
