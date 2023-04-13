import React, {useState} from "react";
import axios from "axios";
import {useNavigate} from "react-router-dom";

const SearchPerson = ({content,setContent}) => {
    const navigate = useNavigate();
    const [url, setURL] = useState('');

    const displaySelectedValues = async () => {
        var dropdown1 = document.getElementById("dropdown1");
        var dropdown2 = document.getElementById("dropdown2");
        var dropdown3 = document.getElementById("dropdown3");

        var selectedValue1 = dropdown1.options[dropdown1.selectedIndex].value;
        var selectedValue2 = dropdown2.options[dropdown2.selectedIndex].value;
        var selectedValue3 = dropdown3.options[dropdown3.selectedIndex].value;

        let data_json;
        data_json = {
            "hall" : selectedValue1,
            "building": selectedValue2,
            "camera": selectedValue3
        }
        axios({
            // Endpoint to send files
            url: `https://demo1-nwe8.onrender.com/upload`,
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
                setURL(res.data.image);
                setContent(res.data)
                // navigate("/");
            })

            // Catch errors if any
            .catch((e) => {
                console.log(e)
                console.log(e.response.status)
            });
    };
    return <div>
        <h1>Search Person</h1>
        <form>
            <div>
            <label htmlFor="dropdown1">Select Hall:</label>
            <select id="dropdown1">
                <option value="howe">Howe Hall</option>
                <option value="risley">Risley Hall</option>
                <option value="lmp">LMP Hall</option>
                <option value="gerard">Gerard Hall</option>
                <option value="sheriff">Sheriff Hall</option>
            </select>
            </div>
            <div>
            <label htmlFor="dropdown2">Select Building:</label>
            <select id="dropdown2">
                <option value="building1">Building 1</option>
                <option value="building2">Building 2</option>
                <option value="building3">Building 3</option>
                <option value="building4">Building 4</option>
                <option value="building5">Building 5</option>
            </select>
            </div>
            <div>
            <label htmlFor="dropdown3">Select Camera:</label>
            <select id="dropdown3">
                <option value="camera1">Camera 1</option>
                <option value="camera2">Camera 2</option>
                <option value="camera3">Camera 3</option>
                <option value="camera4">Camera 4</option>
                <option value="camera5">Camera 5</option>
            </select>
            </div>
            <div>
            <button type="button" onClick={displaySelectedValues}>Submit</button>
            </div>
        </form>
        {url? (
            <div>
                {console.log(content,"content>>>",url)}
                {url && <img src={url} style={{ maxWidth: '50%', height: '50%' }}/>}
                <p>{content['Found Person ']} has been detected in {content['data']['hall']} hall near {content['data']['building']} of {content['data']['camera']}.</p>
            </div>
        ) : (
            <p>Person not found in Camera capture Frame.</p>
        )}
    </div>;
};

export default SearchPerson;
