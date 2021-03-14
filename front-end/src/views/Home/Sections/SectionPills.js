import React from "react";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";

// @material-ui/icons
import EvStationIcon from '@material-ui/icons/EvStation';import Schedule from "@material-ui/icons/Schedule";
import GroupIcon from '@material-ui/icons/Group';
import DriveEtaIcon from '@material-ui/icons/DriveEta';
import List from "@material-ui/icons/List";

// core components
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import NavPills from "components/NavPills/NavPills.js";

import styles from "assets/jss/material-kit-react/views/componentsSections/pillsStyle.js";
import imgStyles from "assets/jss/material-kit-react/views/componentsSections/carouselStyle.js";

import Card from "components/Card/Card.js";
import LocationOn from "@material-ui/icons/LocationOn";
import Carousel from "react-slick";

import image1 from "assets/img/bg.jpg";
import image2 from "assets/img/bg2.jpg";
import image3 from "assets/img/bg3.jpg";

const useStyles = makeStyles(styles);
const useImgStyles = makeStyles(imgStyles);
export default function SectionPills() {
  const classes = useStyles();
  const imgClasses = useImgStyles();
  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: false
  };
  return (
    <div className={classes.section}>
      <div className={classes.container}>
        <div id="navigation-pills">
          <div className={classes.title}>
            <h3><b>About Eevie</b></h3>
          </div>
          <div className={classes.title}>
            <h3>
              <small>Get started</small>
            </h3>
          </div>
          <GridContainer justify="center" align="center" alignItems="center">
            <GridItem xs={12} sm={4} md={4} lg={4}>
              <NavPills
                color="success"
                tabs={[
                  {
                    tabButton: "What is Eevie",
                    tabIcon: EvStationIcon,
                    tabContent: (
                      <span>
                        <p>
                        With our unique key, or card, and the free Eevie App you can access Europe’s largest and most up-to-date network of electric vehicle charging stations.
                        </p>
                        <br />
                        <p>
                        Our map filters work for you. Find over 200,000 charging points in our network and navigate to the one that fits your needs. Now your commute, weekend getaway or road trip across Europe is simple and worry-free.


                        </p>
                      </span>
                    )
                  },
                  {
                    tabButton: "Network",
                    tabIcon: GroupIcon,
                    tabContent: (
                      <span>
                        <p>
                        Charge your electric vehicle wherever you want - our extensive network of EV access points means there’s always a charging station near you.


                        </p>
                        <br />
                        <p>
                        Our partners are pioneers in the mobility sector, which means that you profit from a dense network of charging stations and our tailor-made map.


                        </p>
                      </span>
                    )
                  },
                  {
                    tabButton: "Drivers",
                    tabIcon: DriveEtaIcon,
                    tabContent: (
                      <span>
                        <p>
                        The route planner finds the fastest route based on your car's battery status and brings you to the charging points along your trip when you need them. Download our free Eevie app and use the route planner to plan your next trip.
                        </p>
                      </span>
                    )
                  }
                ]}
              />
            </GridItem>
          </GridContainer>
          
        </div>
      </div>
    </div>
  );
}
