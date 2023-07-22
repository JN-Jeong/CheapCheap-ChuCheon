const express = require("express");
const router = express.Router();
const Items = require("../models/items");

// dmSearch값에 따라 데이터 조회
router.post("/", (req, res) => {
  let params = req.body.params;

  Items.find(
    {
      categories:
        params.category === "전체" ? { $ne: "" } : { $eq: params.category },
    },
    null,
    { skip: (params.pageIndex - 1) * params.pageSize, limit: params.pageSize }
  )
    .sort({ date: -1 })
    .then((items) => {
      let resData = {};
      resData.itemsList = items;
      Items.countDocuments({
        categories:
          params.category === "전체" ? { $ne: "" } : { $eq: params.category },
      })
        .then((count) => {
          resData.itemsLength = count;
          res.send(resData);
        })
        .catch((err) => {
          console.log("데이터 개수 조회 에러 : " + err);
        });
    })
    .catch((err) => res.status(500).send(err));
});

module.exports = router;
