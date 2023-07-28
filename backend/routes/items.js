const express = require("express");
const router = express.Router();
const Items = require("../models/items");

// dmSearch값에 따라 데이터 조회
router.post("/", (req, res) => {
  let params = req.body.params;

  Items.aggregate(
    [
      {
        $match: {
          categories:
            params.category === "전체" ? { $ne: "" } : { $eq: params.category },
        },
      },
      { $skip: (params.pageIndex - 1) * params.pageSize },
      { $limit: params.pageSize },
    ],
    { allowDiskUse: true }
  )
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
    .catch((err) => {
      console.log(err);
    });
});

module.exports = router;
