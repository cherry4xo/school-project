import React from 'react';
import { StyleSheet, Text, FlatList, View, TouchableHighlight, ScrollView } from 'react-native';

import { Entypo } from '@expo/vector-icons';
import { Ionicons } from '@expo/vector-icons';
import { MaterialCommunityIcons } from '@expo/vector-icons';

export default function LibraryStart({ navigation }) {

    const toUserSongs = () => navigation.navigate('Songs')
    const toUserAlbums = () => navigation.navigate('Albums')
    const toUserPlaylists = () => navigation.navigate('Playlists')

    return (
        <View style={{ backgroundColor: 'black' }}>
            <ScrollView contentContainerStyle={styles.container}>
                <View style={styles.line} />
                <TouchableHighlight style={{ width: '80%' }} onPress={toUserSongs}>
                    <View style={[styles.menuItem]}>
                        <View style={{ width: 40, display: 'flex', flexDirection: 'row', justifyContent: 'center' }}>
                            <Entypo name="folder-music" size={24} color="#FF0054" />
                        </View>
                        <Text style={styles.text}>Songs</Text>
                    </View>
                </TouchableHighlight>
                <View style={styles.line} />
                <TouchableHighlight style={{ width: '80%' }} onPress={toUserAlbums}>
                    <View style={[styles.menuItem]}>
                        <View style={{ width: 40, display: 'flex', flexDirection: 'row', justifyContent: 'center' }}>
                            <Ionicons name="albums" size={24} color="#FF0054" />
                        </View>
                        <Text style={styles.text}>Albums</Text>
                    </View>
                </TouchableHighlight>
                <View style={styles.line} />
                <TouchableHighlight style={{ width: '80%' }} onPress={toUserPlaylists}>
                    <View style={[styles.menuItem]}>
                        <View style={{ width: 40, display: 'flex', flexDirection: 'row', justifyContent: 'center' }}>
                            <MaterialCommunityIcons name="playlist-music" size={24} color="#FF0054" />
                        </View>
                        <Text style={styles.text}>Playlists</Text>
                    </View>
                </TouchableHighlight>
                <View style={styles.line} />
            </ScrollView >
        </View>

    )
}

const styles = StyleSheet.create({
    container: {
        width: '100%',
        minHeight: '100%',
        backgroundColor: 'black',
        alignItems: 'center',
        display: 'flex',
        paddingBottom: 50
    },
    text: {
        color: 'white',
        fontFamily: 'Nunito-Bold',
        fontSize: '20pt',
        overflow: 'hidden',
    },
    menuItem: {
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'flex-start',
        width: '100%',
        margin: 8,
    },
    line: {
        borderBottomWidth: 1,
        borderBottomColor: '#5A5A5A',
        width: '80%',
    },
    recentlyAddedAlbums: {
        flexDirection: 'row',
        gap: '1rem',
        flexWrap: "wrap",
        width: '100%',
        display: 'flex',
    }
})