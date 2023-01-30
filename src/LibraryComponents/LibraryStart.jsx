import React from 'react';
import { StyleSheet, Text, FlatList, View, TouchableHighlight, ScrollView } from 'react-native';

import { Entypo } from '@expo/vector-icons';
import { Ionicons } from '@expo/vector-icons';
import { MaterialCommunityIcons } from '@expo/vector-icons';

import Album from '../MusicComponents/AlbumComponent.jsx'

const DATA = [
    {
        id: 'bd7acbea-c1b1-46c2-aed5aa-3ad53abb28ba',
        title: 'First Item',
        pictureDirection: require('../../assets/img/avatar.jpg')
    },
    {
        id: '3ac68afc-c605-48d3-a4f8-fbd9dfh1aa97f63',
        title: 'Second Item',
        pictureDirection: require('../../assets/img/HomeBG.png')
    },
    {
        id: '58694a0f-3da1-471f-bd96-1asd45571e29d72',
        title: 'Third Item',
        pictureDirection: require('../../assets/img/downloadImage.png')
    },
    {
        id: 'bd7acbea-c1b1-46c2-aedsf5-3ad53sdfabb28ba',
        title: 'First Item',
        pictureDirection: require('../../assets/img/avatar.jpg')
    },
    {
        id: '3ac68afc-c605-48d3-a4f8-fbsdfd91aa97f63',
        title: 'Second Item',
        pictureDirection: require('../../assets/img/HomeBG.png')
    },
    {
        id: '58694a0f-3da1-471f-bd96-145571e2sdf9d72',
        title: 'Third Item',
        pictureDirection: require('../../assets/img/downloadImage.png')
    },
];

function AlbumsList() {
    return (
        < View style={[styles.recentlyAddedAlbums, { justifyContent: 'center' }]}>
            {
                DATA.map((item) =>
                    <Album key={item.id} imagePath={item.pictureDirection} albumName={item.title} />
                )
            }
            {
                (DATA.length % 2 != 0) ?
                    <View style={{ width: 140, marginHorizontal: 20 }} />
                    :
                    null
            }
        </View >

    );
}

export default function LibraryStart({ navigation }) {

    const toUserSongs = () => navigation.navigate('Songs')
    const toUserAlbums = () => navigation.navigate('Albums')
    const toUserPlaylists = () => navigation.navigate('Playlists')

    return (
        <View style={{ backgroundColor: 'black' }}>
            <ScrollView contentContainerStyle={styles.container}>
                <View style={styles.line} />
                <TouchableHighlight style={{ width: '100%' }} onPress={toUserSongs}>
                    <View style={[styles.menuItem]}>
                        <View style={{ width: 40, display: 'flex', flexDirection: 'row', justifyContent: 'center' }}>
                            <Entypo name="folder-music" size={24} color="white" />
                        </View>
                        <Text style={styles.text}>Songs</Text>
                    </View>
                </TouchableHighlight>
                <View style={styles.line} />
                <TouchableHighlight style={{ width: '100%' }} onPress={toUserAlbums}>
                    <View style={[styles.menuItem]}>
                        <View style={{ width: 40, display: 'flex', flexDirection: 'row', justifyContent: 'center' }}>
                            <Ionicons name="albums" size={24} color="white" />
                        </View>
                        <Text style={styles.text}>Albums</Text>
                    </View>
                </TouchableHighlight>
                <View style={styles.line} />
                <TouchableHighlight style={{ width: '100%' }} onPress={toUserPlaylists}>
                    <View style={[styles.menuItem]}>
                        <View style={{ width: 40, display: 'flex', flexDirection: 'row', justifyContent: 'center' }}>
                            <MaterialCommunityIcons name="playlist-music" size={24} color="white" />
                        </View>
                        <Text style={styles.text}>Playlists</Text>
                    </View>
                </TouchableHighlight>
                <View style={styles.line} />

                <Text style={[styles.text, { fontSize: 28, marginVertical: 20 }]}>
                    Recently Added:
                </Text>

                <AlbumsList />
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