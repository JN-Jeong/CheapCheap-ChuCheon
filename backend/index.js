// 설정 불러오기
require("dotenv").config();

const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();
const port = process.env.PORT;

app.use(express.static("public"));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// cors 도메인 허용
app.use(
  cors({
    origin: "http://localhost:8080",
    credentials: true,
  })
);

// db 연결
mongoose
  .connect(process.env.MONGO_URI, {
    dbName: process.env.MONGO_DB_NAME,
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => console.log("디비 연결 성공"))
  .catch((err) => console.log(err));

app.use("/items", require("./routes/items"));

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
