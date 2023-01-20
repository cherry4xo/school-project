import React, { useEffect, useState } from "react";
import { View, Button, StyleSheet, TouchableHighlight } from "react-native";

import { useNavigation } from '@react-navigation/native';

import Player from './Player/AudioSlider'
import Track from '../assets/audio/Rammstein_-_DEUTSCHLAND_(musmore.com).mp3'
import trackIcon from '../assets/img/avatar.jpg'

import HomeSVG from "./svgIcons/HomeSVG";
import LibrarySVG from "./svgIcons/LibrarySVG";
import RecPageSVG from "./svgIcons/RecPageSVG";
import SearchSVG from "./svgIcons/SearchSVG";
import SoundSearchSVG from "./svgIcons/SoundSearchSVG";
import { setAudioModeAsync } from "expo-av/build/Audio";

setAudioModeAsync({
    playsInSilentModeIOS: true,
})

export default function NavBar() {

    const [homeImgColor, setHomeImgColor] = useState('red')
    const [searchImgColor, setSearchImgColor] = useState('white')
    const [recImgColor, setRecImgColor] = useState('white')
    const [soundSearchImgColor, setSoundSearchImgColor] = useState('white')
    const [libraryImgColor, setLibraryImgColor] = useState('white')

    const navigation = useNavigation();

    const toHomePage = () => {
        navigation.navigate('HomePage')

        setHomeImgColor('red')
        setSearchImgColor('white')
        setRecImgColor('white')
        setSoundSearchImgColor('white')
        setLibraryImgColor('white')
    }
    const toLibraryPage = () => {
        navigation.navigate('LibraryPage')

        setHomeImgColor('white')
        setSearchImgColor('white')
        setRecImgColor('white')
        setSoundSearchImgColor('white')
        setLibraryImgColor('red')
    }
    const toSoundSearchPage = () => {
        navigation.navigate('SoundSearchPage')

        setHomeImgColor('white')
        setSearchImgColor('white')
        setRecImgColor('white')
        setSoundSearchImgColor('red')
        setLibraryImgColor('white')
    }
    const toRecPage = () => {
        navigation.navigate('RecPage')

        setHomeImgColor('white')
        setSearchImgColor('white')
        setRecImgColor('red')
        setSoundSearchImgColor('white')
        setLibraryImgColor('white')
    }
    const toSearchPage = () => {
        navigation.navigate('SearchPage')

        setHomeImgColor('white')
        setSearchImgColor('red')
        setRecImgColor('white')
        setSoundSearchImgColor('white')
        setLibraryImgColor('white')
    }

    return (
        <View style={styles.Content}>
            <Player trackIcon={trackIcon} trackAuthor={'Rammstein'} trackName={'Deutchland'} audio={Track} />
            <View style={styles.NavBar}>
                <TouchableHighlight
                    style={{ width: 50, height: 50, justifyContent: 'center', alignItems: 'center' }}
                    onPress={toSoundSearchPage}
                >
                    <SoundSearchSVG fill={soundSearchImgColor} />
                </TouchableHighlight>
                <TouchableHighlight
                    style={{ width: 50, height: 50, justifyContent: 'center', alignItems: 'center' }}
                    onPress={toRecPage}
                >
                    <RecPageSVG fill={recImgColor} />
                </TouchableHighlight>
                <TouchableHighlight
                    style={{ width: 50, height: 50, justifyContent: 'center', alignItems: 'center' }}
                    onPress={toHomePage}
                >
                    <HomeSVG fill={homeImgColor} />
                </TouchableHighlight>
                <TouchableHighlight
                    style={{ width: 50, height: 50, justifyContent: 'center', alignItems: 'center' }}
                    onPress={toLibraryPage}
                >
                    <LibrarySVG fill={libraryImgColor} />
                </TouchableHighlight>
                <TouchableHighlight
                    style={{ width: 50, height: 50, justifyContent: 'center', alignItems: 'center' }}
                    onPress={toSearchPage}
                >
                    <SearchSVG fill={searchImgColor} />
                </TouchableHighlight>
            </View>
        </View >
    )
}

const styles = StyleSheet.create({
    Content: {
        width: '100%',
    },
    NavBar: {
        width: '100%',
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'flex-end',
        justifyContent: "space-around",
        paddingTop: 5,
        borderTopColor: 'rgb(96,96,96)',
        borderTopWidth: '1px',
    },
})