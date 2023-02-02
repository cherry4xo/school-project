import React, { useEffect, useState } from "react";
import { View, Text, StyleSheet, TouchableHighlight } from "react-native";

import { useNavigation } from '@react-navigation/native';

import { Ionicons } from '@expo/vector-icons';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { MaterialIcons } from '@expo/vector-icons';

export default function NavBar() {

    const [homeImg, setHomeImg] = useState('home-sharp')
    const [searchImg, setSearchImg] = useState('search-outline')
    const [recImg, setRecImg] = useState('favorite-outline')
    const [soundSearchImg, setSoundSearchImg] = useState('record-circle-outline')
    const [libraryImg, setLibraryImg] = useState('library-outline')

    const navigation = useNavigation();

    const [homeColor, setHomeColor] = useState('#FF0054')
    const [searchColor, setSearchColor] = useState('white')
    const [recColor, setRecColor] = useState('white')
    const [soundSearchColor, setSoundSearchColor] = useState('white')
    const [libraryColor, setLibraryColor] = useState('white')

    const toHomePage = () => {
        navigation.navigate('HomePage')

        setHomeImg('home-sharp')
        setSearchImg('search-outline')
        setRecImg('favorite-outline')
        setSoundSearchImg('record-circle-outline')
        setLibraryImg('library-outline')

        setHomeColor('#FF0054')
        setSearchColor('white')
        setRecColor('white')
        setSoundSearchColor('white')
        setLibraryColor('white')
    }
    const toLibraryPage = () => {
        navigation.navigate('LibraryPage')

        setHomeImg('ios-home-outline')
        setSearchImg('search-outline')
        setRecImg('favorite-outline')
        setSoundSearchImg('record-circle-outline')
        setLibraryImg('library')

        setHomeColor('white')
        setSearchColor('white')
        setRecColor('white')
        setSoundSearchColor('white')
        setLibraryColor('#FF0054')
    }
    const toSoundSearchPage = () => {
        navigation.navigate('SoundSearchPage')

        setHomeImg('ios-home-outline')
        setSearchImg('search-outline')
        setRecImg('favorite-outline')
        setSoundSearchImg('record-circle')
        setLibraryImg('library-outline')

        setHomeColor('white')
        setSearchColor('white')
        setRecColor('white')
        setSoundSearchColor('#FF0054')
        setLibraryColor('white')
    }
    const toRecPage = () => {
        navigation.navigate('RecPage')

        setHomeImg('ios-home-outline')
        setSearchImg('search-outline')
        setRecImg('favorite')
        setSoundSearchImg('record-circle-outline')
        setLibraryImg('library-outline')

        setHomeColor('white')
        setSearchColor('white')
        setRecColor('#FF0054')
        setSoundSearchColor('white')
        setLibraryColor('white')
    }
    const toSearchPage = () => {
        navigation.navigate('SearchPage')

        setHomeImg('ios-home-outline')
        setSearchImg('search')
        setRecImg('favorite-outline')
        setSoundSearchImg('record-circle-outline')
        setLibraryImg('library-outline')

        setHomeColor('white')
        setSearchColor('#FF0054')
        setRecColor('white')
        setSoundSearchColor('white')
        setLibraryColor('white')
    }

    return (
        <View style={styles.Content}>
            <View style={styles.NavBar}>
                <TouchableHighlight
                    style={{ width: 60, height: 50, justifyContent: 'center', alignItems: 'center' }}
                    onPress={toSoundSearchPage}
                >
                    <View style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <MaterialCommunityIcons name={soundSearchImg} size={24} color={soundSearchColor} />
                        <Text style={[styles.text, { fontSize: 10 }]}>Find Song</Text>
                    </View>
                </TouchableHighlight>
                <TouchableHighlight
                    style={{ width: 60, height: 50, justifyContent: 'center', alignItems: 'center' }}
                    onPress={toRecPage}
                >
                    <View style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <MaterialIcons name={recImg} size={24} color={recColor} />
                        <Text style={[styles.text, { fontSize: 10 }]}>Suggestion</Text>
                    </View>

                </TouchableHighlight>
                <TouchableHighlight
                    style={{ width: 60, height: 50, justifyContent: 'center', alignItems: 'center' }}
                    onPress={toHomePage}
                >
                    <View style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <Ionicons name={homeImg} size={24} color={homeColor} />
                        <Text style={[styles.text, { fontSize: 10 }]}>Home</Text>
                    </View>
                </TouchableHighlight>
                <TouchableHighlight
                    style={{ width: 60, height: 50, justifyContent: 'center', alignItems: 'center' }}
                    onPress={toLibraryPage}
                >
                    <View style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <Ionicons name={libraryImg} size={24} color={libraryColor} />
                        <Text style={[styles.text, { fontSize: 10 }]}>Library</Text>
                    </View>
                </TouchableHighlight>
                <TouchableHighlight
                    style={{ width: 60, height: 50, justifyContent: 'center', alignItems: 'center' }}
                    onPress={toSearchPage}
                >
                    <View style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <Ionicons name={searchImg} size={24} color={searchColor} />
                        <Text style={[styles.text, { fontSize: 10 }]}>Search</Text>
                    </View>
                </TouchableHighlight>
            </View>
        </View >
    )
}

const styles = StyleSheet.create({
    Content: {
        width: '100%',
        height: 50,
        zIndex: 5
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
    text: {
        color: 'white',
        fontSize: 24,
        fontFamily: 'Nunito-Bold',
    }
})