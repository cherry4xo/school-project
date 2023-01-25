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

    const toHomePage = () => {
        navigation.navigate('HomePage')

        setHomeImg('home-sharp')
        setSearchImg('search-outline')
        setRecImg('favorite-outline')
        setSoundSearchImg('record-circle-outline')
        setLibraryImg('library-outline')
    }
    const toLibraryPage = () => {
        navigation.navigate('LibraryPage')

        setHomeImg('ios-home-outline')
        setSearchImg('search-outline')
        setRecImg('favorite-outline')
        setSoundSearchImg('record-circle-outline')
        setLibraryImg('library')
    }
    const toSoundSearchPage = () => {
        navigation.navigate('SoundSearchPage')

        setHomeImg('ios-home-outline')
        setSearchImg('search-outline')
        setRecImg('favorite-outline')
        setSoundSearchImg('record-circle')
        setLibraryImg('library-outline')
    }
    const toRecPage = () => {
        navigation.navigate('RecPage')

        setHomeImg('ios-home-outline')
        setSearchImg('search-outline')
        setRecImg('favorite')
        setSoundSearchImg('record-circle-outline')
        setLibraryImg('library-outline')
    }
    const toSearchPage = () => {
        navigation.navigate('SearchPage')

        setHomeImg('ios-home-outline')
        setSearchImg('search')
        setRecImg('favorite-outline')
        setSoundSearchImg('record-circle-outline')
        setLibraryImg('library-outline')
    }

    return (
        <View style={styles.Content}>
            <View style={styles.NavBar}>
                <TouchableHighlight
                    style={{ width: 60, height: 50, justifyContent: 'center', alignItems: 'center' }}
                    onPress={toSoundSearchPage}
                >
                    <View style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <MaterialCommunityIcons name={soundSearchImg} size={24} color="white" />
                        <Text style={[styles.text, { fontSize: 10 }]}>Find Song</Text>
                    </View>
                </TouchableHighlight>
                <TouchableHighlight
                    style={{ width: 60, height: 50, justifyContent: 'center', alignItems: 'center' }}
                    onPress={toRecPage}
                >
                    <View style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <MaterialIcons name={recImg} size={24} color="white" />
                        <Text style={[styles.text, { fontSize: 10 }]}>Suggestion</Text>
                    </View>

                </TouchableHighlight>
                <TouchableHighlight
                    style={{ width: 60, height: 50, justifyContent: 'center', alignItems: 'center' }}
                    onPress={toHomePage}
                >
                    <View style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <Ionicons name={homeImg} size={24} color="white" />
                        <Text style={[styles.text, { fontSize: 10 }]}>Home</Text>
                    </View>
                </TouchableHighlight>
                <TouchableHighlight
                    style={{ width: 60, height: 50, justifyContent: 'center', alignItems: 'center' }}
                    onPress={toLibraryPage}
                >
                    <View style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <Ionicons name={libraryImg} size={24} color="white" />
                        <Text style={[styles.text, { fontSize: 10 }]}>Library</Text>
                    </View>
                </TouchableHighlight>
                <TouchableHighlight
                    style={{ width: 60, height: 50, justifyContent: 'center', alignItems: 'center' }}
                    onPress={toSearchPage}
                >
                    <View style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <Ionicons name={searchImg} size={24} color="white" />
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