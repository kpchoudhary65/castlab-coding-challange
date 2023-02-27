import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Button from 'react-bootstrap/Button';
import { Table } from 'react-bootstrap';

const Home = () => {

  const [data, setData] = useState([]);


  useEffect(() => {
   _getfunc()
  }, []);

  const _getfunc=()=>{
     axios.get('http://localhost:8080', {},

      {
        headers: {
          "Access-Control-Allow-Origin": true
        },
      })
      .then(response => setData(response.data))
      .catch(error => console.log(error))
  }


  const _postfunc = async () => {

   const res = await fetch('http://localhost:8080', {
      method: 'POST',
      headers: {},
      body: JSON.stringify(data)
    })
    console.log(res,'res')
    _getfunc()
  }


  return (
    <div>
    <div className="topmargin">
      <Button variant="warning" onClick={() => _postfunc()}>Send Mail</Button>
      </div>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>TO</th>
            <th>FROM EMAIL</th>
            <th>SUBJECT</th>
            <th>BODY</th>

          </tr>
        </thead>
        <tbody>
  {data.map((item, index) => (
          <tr key={index}>
            <td>{item?.to}</td>
            <td>{item?.from_email}</td>
            <td>{item?.subject}</td>
            <td dangerouslySetInnerHTML={{ __html: item?.body }}/>
          </tr>
        ))}
        </tbody>
      </Table>
    </div>

  );
}



export default Home;
