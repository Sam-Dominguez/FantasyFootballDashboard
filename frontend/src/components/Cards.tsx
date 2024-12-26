import React from 'react';
import { Link } from 'react-router-dom';

function Cards() {

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
                            <h5 className="card-title">Points Left on Bench</h5>
                            <p className="card-text">League-wide analysis of points left on bench each week</p>
                            <Link to="/points-on-bench" className="btn btn-primary">Open</Link>
                        </div>
                    </div>
            </div>
        </div>
    </div>
  );
}

export default Cards;
