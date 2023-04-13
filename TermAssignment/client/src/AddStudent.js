import React, {useState} from "react";
import axios from "axios";
import {useNavigate} from "react-router-dom";

const AddStudent = () => {
    const [id, setId] = useState('');
    const [name, setName] = useState('');
    const [number, setNumber] = useState('');
    const [email, setEmail] = useState('');
    const navigate = useNavigate();

    function backToHome() {
        navigate("/");
    }
    const handleSubmit = async () => {
            let data_json;
            data_json = {
                "id" : id,
                "name": name,
                "number": number,
                "email" : email
            }
        axios({
            // Endpoint to send files
            url: `https://demo1-nwe8.onrender.com/add_students`,
            method: "POST",
            data: data_json,
            headers: {
                'Content-Type': 'application/json',
                "Access-Control-Allow-Origin": "*"
            }
        })
            // Handle the response from backend here
            .then((res) => {
                console.log(res,"res>>>>>>")
                navigate("/");
            })

            // Catch errors if any
            .catch((e) => {
                console.log(e)
                console.log(e.response.status)
            });
    };

    return <div>
        <h1>Add Student</h1>
        <form >
            <label>
                Id:
                <input type="text" value={id} onChange={(e) => setId(e.target.value)} />
            </label>
            <br />
            <label>
                Name:
                <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
            </label>
            <br />
            <label>
                Number:
                <input type="text" value={number} onChange={(e) => setNumber(e.target.value)} />
            </label>
            <br />
            <label>
                Email:
                <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} />
            </label>
            <br />
            <button type="button" onClick={handleSubmit}>Submit</button>
        </form>
    </div>;
};

export default AddStudent;
