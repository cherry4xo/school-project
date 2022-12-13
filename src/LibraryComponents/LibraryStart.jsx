import React from 'react';
import { StyleSheet, Text, View, TouchableHighlight } from 'react-native';


export default function LibraryStart({ navigation }) {

    const toUserSongs = () => navigation.navigate('Songs')
    const toUserAlbums = () => navigation.navigate('Albums')
    const toUserPlaylists = () => navigation.navigate('Playlists')

    return (
        <View style={styles.container}>
            <TouchableHighlight onPress={toUserSongs} style={[styles.menuItem, { backgroundColor: '#BC312E', }]}>
                <Text style={styles.text}>Songs</Text>
            </TouchableHighlight>
            <View style={styles.itemsPair}>
                <TouchableHighlight onPress={toUserAlbums} style={[styles.menuItem, { backgroundColor: '#182F7F', }]}>
                    <Text style={styles.text}>Albums</Text>
                </TouchableHighlight>
                <TouchableHighlight onPress={toUserPlaylists} style={[styles.menuItem, { backgroundColor: '#5A9D36', }]}>
                    <Text style={styles.text}>Playlists</Text>
                </TouchableHighlight>
            </View >
        </View >
    )
}

const styles = StyleSheet.create({
    container: {
        width: '100%',
        height: '100%',
        flex: 1,
        backgroundColor: 'black',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
    },
    text: {
        color: 'white',
        fontFamily: 'Nunito-Bold',
        fontSize: '20pt'
    },
    itemsPair: {
        display: 'flex',
        flexDirection: 'row',
    },
    menuItem: {
        width: 150,
        height: 150,
        borderRadius: 25,

        alignItems: 'center',
        justifyContent: 'center',

        margin: 8,
    }
})