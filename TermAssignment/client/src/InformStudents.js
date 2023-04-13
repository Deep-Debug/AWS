import React, {useEffect, useState} from "react";
import axios from "axios";
import {useNavigate} from "react-router-dom";
import {Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow} from "@mui/material";

const InformStudent = ({content,setContent}) => {
    const [email, setEmail] = useState('');
    const [studentList, setStudentList] = useState([]);
    const navigate = useNavigate();

    function backToHome() {
        navigate("/");
    }
    const handleSubmit = async (data) => {
        console.log(data,"data>>>>>1",content)
        let data_json;
        data_json = {
            "email" : data,
            "content" : content
        }
        axios({
            // Endpoint to send files
            url: `https://demo1-nwe8.onrender.com/notify_students`,
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

    useEffect(()=>{
        axios({
            // Endpoint to send files
            url: `https://demo1-nwe8.onrender.com/get_students`,
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
                "Access-Control-Allow-Origin": "*"
            }
        })
            // Handle the response from backend here
            .then((res) => {
                console.log(res,"res>>>>>>")
                setStudentList(res.data["data"][0])
            })

            // Catch errors if any
            .catch((e) => {
                console.log(e)
                console.log(e.response.status)
            });
    },[])

    return <div>
        <h1>Send Message</h1>
        <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
                <TableHead>
                    <TableRow>
                        <TableCell align="right">Id</TableCell>
                        <TableCell align="right">Name</TableCell>
                        <TableCell align="right">Number</TableCell>
                        <TableCell align="right">Email</TableCell>
                        <TableCell align="right">Inform</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {studentList.map((row) => (
                        <TableRow
                            key={row.id}
                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                        >
                            <TableCell component="th" scope="row">
                                {row.id}
                            </TableCell>
                            <TableCell align="right">{row.name}</TableCell>
                            <TableCell align="right">{row.number}</TableCell>
                            <TableCell align="right">{row.email}</TableCell>
                            <TableCell align="right">
                                <button type="button" onClick={()=>handleSubmit(row.email)}>Inform</button>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    </div>;
};

export default InformStudent;
