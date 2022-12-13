import React from 'react';

import { StyleSheet, Text, View, SafeAreaView } from 'react-native';

//rooting
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

const Tab = createBottomTabNavigator();

//fonts
import { useFonts } from 'expo-font';
import AppLoading from 'expo-app-loading'

//components
import NavBar from './src/NavBar';
import HomePage from './src/Roots/HomePage';
import LibraryPage from './src/Roots/LibraryPage'
import RecPage from './src/Roots/RecPage'
import SearchPage from './src/Roots/SearchPage'
import SoundSearchPage from './src/Roots/SoundSearchPage'
import HomeSVG from './src/svgIcons/HomeSVG';

export default function App() {

  let [fontsLoaded] = useFonts({
    'Nunito-Regular': require('./assets/fonts/Nunito/Nunito-Regular.ttf'),
    'Nunito-Bold': require('./assets/fonts/Nunito/Nunito-Bold.ttf')
  })

  if (!fontsLoaded) return <AppLoading />

  return (
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
    </SafeAreaView >
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