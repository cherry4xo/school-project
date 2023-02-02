import React, { useEffect, useState } from 'react';

import { StyleSheet, Text, View, SafeAreaView } from 'react-native';

//rooting
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

const Tab = createBottomTabNavigator();

//fonts
import { useFonts } from 'expo-font'
import AppLoading from 'expo-app-loading'

//components
import NavBar from './src/NavBar';
import HomePage from './src/Roots/HomePage';
import LibraryPage from './src/Roots/LibraryPage'
import RecPage from './src/Roots/RecPage'
import SearchPage from './src/Roots/SearchPage'
import SoundSearchPage from './src/Roots/SoundSearchPage'

import Player from './src/Player/AudioSlider'
import Track from './assets/audio/Rammstein_-_DEUTSCHLAND_(musmore.com).mp3'
import trackIcon from './assets/img/avatar.jpg'

import { setAudioModeAsync } from "expo-av/build/Audio";

setAudioModeAsync({
  playsInSilentModeIOS: true,
})

export default function App() {

  let [fontsLoaded] = useFonts({
    'Nunito-Regular': require('./assets/fonts/Nunito/Nunito-Regular.ttf'),
    'Nunito-Bold': require('./assets/fonts/Nunito/Nunito-Bold.ttf'),
    'Nunito-Light': require('./assets/fonts/Nunito/Nunito-Light.ttf'),
    'Nunito-Medium': require('./assets/fonts/Nunito/Nunito-Medium.ttf'),
  })

  if (!fontsLoaded) return <AppLoading />

  return (
    <View>
      <SafeAreaView style={styles.container}>

        <NavigationContainer>
          <Tab.Navigator
            initialRouteName='Home'
            tabBar={() => <NavBar />}

            screenOptions={{

            }}

          >
            <Tab.Screen
              name="HomePage"
              component={HomePage}
              options={{
                title: 'Home',
                headerStyle: {
                  backgroundColor: 'black',
                  elevation: 0,
                  shadowOffset: {
                    width: 0,
                    height: 0
                  }
                },
                headerTintColor: 'white',
                headerTitleStyle: {
                  fontFamily: 'Nunito-Bold',
                },
              }}
            />
            <Tab.Screen
              name="LibraryPage"
              component={LibraryPage}
              options={{
                headerShown: false
              }}
            />
            <Tab.Screen
              name="RecPage"
              component={RecPage}
              options={{
                title: 'Recomendations',
                headerStyle: {
                  backgroundColor: 'black',
                  elevation: 0,
                  shadowOffset: {
                    width: 0,
                    height: 0
                  }
                },
                headerTintColor: 'white',
                headerTitleStyle: {
                  fontFamily: 'Nunito-Bold',
                },
              }}
            />
            <Tab.Screen
              name="SoundSearchPage"
              component={SoundSearchPage}
              options={{
                title: 'Search Sound',
                headerStyle: {
                  backgroundColor: 'black',
                  elevation: 0,
                  shadowOffset: {
                    width: 0,
                    height: 0
                  }
                },
                headerTintColor: 'white',
                headerTitleStyle: {
                  fontFamily: 'Nunito-Bold',
                },
              }}
            />
            <Tab.Screen
              name="SearchPage"
              component={SearchPage}
              options={{
                title: 'Search',
                headerStyle: {
                  backgroundColor: 'black',
                  elevation: 0,
                  shadowOffset: {
                    width: 0,
                    height: 0
                  }
                },
                headerTintColor: 'white',
                headerTitleStyle: {
                  fontFamily: 'Nunito-Bold',
                },
              }}
            />
          </Tab.Navigator>
        </NavigationContainer>
        <Player trackIcon={trackIcon} trackAuthor={'Rammstein'} trackName={'Deutchlandffffffffffffffdfdfsdgdsgsd'} audio={Track} />
      </SafeAreaView >
    </View>

  );
}

const styles = StyleSheet.create({
  container: {
    width: '100%',
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: 'black'
  },
});