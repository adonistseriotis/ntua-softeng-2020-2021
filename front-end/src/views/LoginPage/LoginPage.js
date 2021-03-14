import React, { useState } from "react";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";

import Header from "components/Header/Header.js";
import Footer from "components/Footer/Footer.js";
import GridContainer from "components/Grid/GridContainer.js";
import GridItem from "components/Grid/GridItem.js";
import Button from "components/CustomButtons/Button.js";
import Card from "components/Card/Card.js";
import CardBody from "components/Card/CardBody.js";
import CardHeader from "components/Card/CardHeader.js";
import CardFooter from "components/Card/CardFooter.js";

import styles from "assets/jss/material-kit-react/views/loginPage.js";

import axiosInstance from "../../axiosApi";


import {useForm} from "react-hook-form";
import TextField from "@material-ui/core/TextField";
import { ThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import { green } from '@material-ui/core/colors';
import { Redirect } from "react-router";

const useStyles = makeStyles(styles);

const theme = createMuiTheme({
  palette: {
    primary: green
  },
});


export default function LoginPage(props) {
  const [cardAnimaton, setCardAnimation] = useState("cardHidden");
  setTimeout(function() {
    setCardAnimation("");
  }, 700);
  const {register, handleSubmit} = useForm();
  const [loggedIn, setLoggedIn] = useState(false);
  const [authError, setAuthError] = useState(false);
  const classes = useStyles();
  const { ...rest } = props;
  const usernameProps = ["kwstas"];

  const onSubmit = (e) => {
    try {
      const response = axiosInstance.post('login/', {
        username: e.username,
        password: e.password
      })
      .then(res => {
        if (!res) {
          setAuthError(true);
          return;
        }
        console.log("kwstas")
        console.log(res);
        setAuthError(false);
        localStorage.setItem("isLoggedIn", true);
        localStorage.setItem("username", e.username);
        console.log("kwstas")
        axiosInstance.defaults.headers['Authorization'] ="JWT " + res.data.access;
        console.log("kwstas")
        localStorage.setItem('access_token', res.data.access);
        localStorage.setItem('refresh_token', res.data.refresh); 
        const timer = setTimeout(()=> {
          setLoggedIn(true);
        }, 800);
       })
       .catch(error => {
         console.log(error)
         setAuthError(true);
       })
    } catch (error) {
      throw error;
    }

    
  }

  let textfieldUsername;
  if (authError) {
    textfieldUsername = <TextField
    error
    margin="normal"
    inputRef={register}
    required
    fullWidth
    name="username"
    label="Username"
    type="username"
    id="username"
    autoComplete="username"
  />;
  } else {
    textfieldUsername = <TextField
        margin="normal"
        inputRef={register}
        required
        fullWidth
        name="username"
        label="Username"
        type="username"
        id="username"
        autoComplete="username"
        autoFocus
      />;
  }

  let textfieldPassword;
  if (authError) {
    textfieldPassword = <TextField
    error
    margin="normal"
    inputRef={register}
    required
    fullWidth
    name="password"
    label="Password"
    type="password"
    id="password"
    autoComplete="current-password"
    autoFocus
    helperText = "Incorrect username or passowrd"

  />;
  } else {
    textfieldPassword = <TextField
        margin="normal"
        inputRef={register}
        required
        fullWidth
        name="password"
        label="Password"
        type="password"
        id="password"
        autoComplete="current-password"
      />;
  }
  

  return (
    <div>
      {loggedIn && <Redirect to = {'/'}/>}
      <Header
        absolute
        color="success"
        brand="eevie"
        {...rest}
      />
      <div
        style={{
          backgroundColor: "#fcfcfc",
          backgroundSize: "cover",
          backgroundPosition: "top center"
        }}
      >
        <div className={classes.container}>
          <GridContainer justify="center">
            <GridItem xs={12} sm={12} md={4}>
              <Card className={classes[cardAnimaton]}>
                <form className={classes.form} onSubmit={handleSubmit( onSubmit )}>
                  <CardHeader color="success" className={classes.cardHeader}>
                    <h4>Welcome back!</h4>
                    <div className={classes.socialLine}>
                      <Button
                        justIcon
                        href="#pablo"
                        target="_blank"
                        color="transparent"
                        onClick={e => e.preventDefault()}
                      >
                        <i className={"fab fa-twitter"} />
                      </Button>
                      <Button
                        justIcon
                        href="#pablo"
                        target="_blank"
                        color="transparent"
                        onClick={e => e.preventDefault()}
                      >
                        <i className={"fab fa-facebook"} />
                      </Button>
                      <Button
                        justIcon
                        href="#pablo"
                        target="_blank"
                        color="transparent"
                        onClick={e => e.preventDefault()}
                      >
                        <i className={"fab fa-google-plus-g"} />
                      </Button>
                    </div>
                  </CardHeader>
                  <CardBody>
                  <ThemeProvider theme = { theme }>
                    { textfieldUsername }
                    { textfieldPassword }
                    </ThemeProvider>
                  </CardBody>
                  <CardFooter className={classes.cardFooter}>
                    <Button
                    simple
                    size = "lg"
                    type="submit"
                    variant="contained"
                    color="success"
                  >
                    Sign In
                  </Button>
                  </CardFooter>
                </form>
              </Card>
            </GridItem>
          </GridContainer>
        </div>
        <Footer blackFont />
      </div>
    </div>
  );
}