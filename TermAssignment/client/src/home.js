import React from "react";
import axios from "axios";
import {useNavigate} from "react-router-dom";



const Home = () => {
    const navigate = useNavigate();

    function handleButton1() {
        navigate("/addStudent");

    }
    function handleButton4() {
        navigate("/addCriminal");

    }
    function handleButton2() {
        navigate("/searchPerson");

    }
    function handleButton3() {
        navigate("/informPerson");
    }

    return <div>
        <h1>Dalsafe Portal</h1>
        <div>
            <button type="button" onClick={handleButton1}>Add Student</button>
        </div>
        <div>
            <button type="button" onClick={handleButton4}>Add Criminal</button>
        </div>
        <div>
            <button type="button" onClick={handleButton2}>Search Person</button>
        </div>
        <div>
            <button type="button" onClick={handleButton3}>Inform Student</button>
        </div>

    </div>;
};

export default Home;
