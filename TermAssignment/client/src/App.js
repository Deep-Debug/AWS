import logo from './logo.svg';
import './App.css';
import {BrowserRouter, Route, Routes} from "react-router-dom";
import Home from "./home";
import AddStudent from "./AddStudent";
import SearchPerson from "./SearchPerson";
import InformStudent from "./InformStudents";
import {useState} from "react";
import AddCriminal from "./AddCriminal";

function App() {
    const[content,setContent] = useState('');
  return (
    <div>
        <BrowserRouter>
        <Routes>
      <Route path="/" element={<Home/>} exact />
      <Route path="/addStudent" element={<AddStudent/>} exact />
      <Route path="/addCriminal" element={<AddCriminal/>} exact />
      <Route path="/searchPerson" element={<SearchPerson content={content} setContent={setContent}/>} exact />
      <Route path="/informPerson" element={<InformStudent content={content} setContent={setContent}/>} exact />
        </Routes>
        </BrowserRouter>
    </div>
  );
}

export default App;
