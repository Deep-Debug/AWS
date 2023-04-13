import React, {useState} from "react";
import axios from "axios";
import {useNavigate} from "react-router-dom";

const AddCriminal = () => {
    const navigate = useNavigate();
    const [name, setName] = useState('');

    function backToHome() {
        navigate("/");
    }
    const [selectedFile, setSelectedFile] = useState(null);
    const [isFilePicked, setIsFilePicked] = useState(false);
    const [previewSource, setPreviewSource] = useState(null);

    const changeHandler = (event) => {
        const file = event.target.files[0];
        previewFile(file);
        setSelectedFile(file);
        setIsFilePicked(true);
    };

    const previewFile = (file) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = () => {
            setPreviewSource(reader.result);
        };
    };

    const handleSubmission = () => {
        const formData = new FormData();
        formData.append('name',name)
        formData.append('image', selectedFile);
        console.log(formData,"formData>>>>>>>>")
        axios.post('https://demo1-nwe8.onrender.com/add_criminal', formData).then((response) => {
            console.log(response);
        });
    };

    return <div>
        <h1>Add Criminal</h1>
        <div>
            <label>
                Name:
                <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
            </label>
            <br />
            <input type="file" name="image" onChange={changeHandler} />
            {isFilePicked ? (
                <div>
                    {previewSource && <img src={previewSource} alt="Preview" style={{ maxWidth: '50%', height: '50%' }} />}
                    <button onClick={handleSubmission}>Upload</button>
                </div>
            ) : (
                <p>Please select an image to upload</p>
            )}
        </div>
    </div>;
};

export default AddCriminal;
