const express = require("express");
const router = express.Router();
const Items = require("../models/items");
const { ObjectId } = require("mongodb");

// dmSearch값에 따라 데이터 조회
router.post("/selectListOnBoard", (req, res) => {
  let params = req.body.params;

  Items.aggregate(
    [
      {
        $match: {
          categories:
            params.category === "전체" ? { $ne: "" } : { $eq: params.category },
        },
      },
      {
        $sort: {
          date: -1,
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

router.post("/selectOneById", (req, res) => {
  let id = req.body.params;

  Items.aggregate([
    {
      $match: {
        _id: new ObjectId(id),
      },
    },
  ])
    .then((item) => {
      let resData = {};
      resData.item = item;
      res.send(resData);
    })
    .catch((err) => {
      console.log(err);
    });
});

module.exports = router;
