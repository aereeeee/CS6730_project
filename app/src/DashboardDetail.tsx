import React, { useEffect, useState } from "react";
import dialogueDataOrigin from "./assets/dialogue.json";
import "./Dashboard.scss";
import * as d3 from "d3";
import classNames from "classnames";
import { SentimentVis } from "./SentimentVis";
import { WaffleChart } from "./WaffleChart";
import { Tooltip } from "antd";
import { colorGenderMap } from "./utils/data";

export const DashboardDetail = ({ item }) => {
  const {
    id,
    title,
    lines,
    data,
    totalWordCount,
    genderWordCount,
    genderWordPercent,
  } = item;

  const [selectedGender, setGender] = useState();

  const onHoverGenderButton = (e) => {
    setGender(e.target.getAttribute("data-gender"));
  };

  return (
    <div className="dashboard-modal">
      <div className="left">
        <div className="head-title">{data.title}</div>
        <div className="main-info">
          <div
            className="poster"
            style={{
              backgroundImage: `url("${data.image}")`,
            }}
          ></div>
          <div className="waffle" style={{ width: "150px", height: "150px" }}>
            <WaffleChart
              data={lines}
              binSize={15}
              chunkSize={100}
              index={0}
              transition={false}
            />
          </div>
        </div>
        <div>
          <div className="item">{data.plot}</div>
        </div>
      </div>
      <div className="right">
        <div
          className={classNames("legend", {
            active: !!selectedGender,
          })}
          onMouseLeave={() => {
            setGender(null);
          }}
        >
          <div
            className={classNames("legend-item female", {
              active: selectedGender === "female",
            })}
            data-gender="female"
            onMouseOver={onHoverGenderButton}
          >
            Female
          </div>
          <div
            className={classNames("legend-item male", {
              active: selectedGender === "male",
            })}
            data-gender="male"
            onMouseOver={onHoverGenderButton}
          >
            Male
          </div>
          <div
            className={classNames("legend-item na", {
              active: selectedGender === "na",
            })}
            data-gender="na"
            onMouseOver={onHoverGenderButton}
          >
            Unknown
          </div>
        </div>
        <div className="section script-proportion">
          <div className="title">Gender Dialogue Amount Ratio</div>
          {/* <div className="description">
            The dialogue amount for each gender is calculated based on the
            number of words spoken by each character.
          </div> */}
          <div
            className={classNames("vis-section proportion-vis", {
              active: !!selectedGender,
            })}
            onMouseLeave={() => {
              setGender(null);
            }}
          >
            <span>0%</span>
            {Object.entries(genderWordPercent).map(([key, val]) => (
              <Tooltip
                placement="bottom"
                title={(val * 100).toFixed(2) + "%"}
                key={key}
              >
                <div
                  key={key}
                  className={classNames("bar", key, {
                    active: selectedGender === key,
                  })}
                  data-gender={key}
                  style={{
                    width: `${val * 100}%`,
                    background: colorGenderMap[key],
                  }}
                  onMouseOver={onHoverGenderButton}
                ></div>
              </Tooltip>
            ))}
            <span>100%</span>
          </div>
        </div>
        <div className="section script-sentiment">
          <div className="title">Dialogue Emotion Analysis</div>
          {/* <div className="description">
            Comparing the emotions expressed in the dialogues of male and female
            characters.
          </div> */}
          <div className="vis-section">
            <SentimentVis
              item={item}
              activeGender={selectedGender}
            ></SentimentVis>
          </div>
        </div>
      </div>
    </div>
  );
};
