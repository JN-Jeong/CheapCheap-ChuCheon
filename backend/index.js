const express = require('express');
const mongoose = require('mongoose');

const app = express();
const port = 3000;

// db 연결
mongoose
.connect(
    'mongodb://localhost:27017',
    {
        dbName:'test'
    }
)
.then(()=>console.log('몽고디비 연결함'))
.catch((err)=>console.log(err));

// 해당 과정을 통해 컬렉션의 구조를 정함
const testSchema = new mongoose.Schema({
    _id: {type:Number, required:true},
    content: {type:String}
},
{
    collection: 'test'
});
const Test = mongoose.model('Test', testSchema);

app.get('/', (req, res) => {
    res.send('Hello World!!');
})

app.get('/all', (req, res) => {
    Test.find({})
    .then(datas=>{
        res.send(datas);
    });
})

app.get('/:id', (req, res) => {
    Test.find({_id:req.params.id})
    .then(datas=>{
        if(datas.length != 0){
            res.send(datas);
        }
        else{
            res.send('데이터 못 찾음');
        }
    });
})

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`);
})


// 참고
// https://poiemaweb.com/mongoose