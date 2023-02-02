import React from "react";
import { useEffect } from "react";
import { StyleSheet, Text, View, Image, TouchableHighlight, ScrollView, Dimensions } from 'react-native';

import Song from './SongComponent.jsx'

const windowWidth = Dimensions.get('window').width;
const windowHeight = Dimensions.get('window').height;

const DATA = [
    {
        id: 'bd7acbea-c1b1-46c2-aed5aa-3ad53abb28ba',
        title: 'First Item',
        pictureDirection: require('../../assets/img/avatar.jpg'),
        name: 'Song 1 lkjfdssdlkfjslkfjdlslkdlkdsjl'
    },
    {
        id: '3ac68afc-c605-48d3-a4f8-fbd9dfh1aa97f63',
        title: 'Second Item',
        pictureDirection: require('../../assets/img/HomeBG.png'),
        name: 'Song 2'
    },
    {
        id: '58694a0f-3da1-471f-bd96-1asd45571e29d72',
        title: 'Third Item',
        pictureDirection: require('../../assets/img/downloadImage.png'),
        name: 'Song 3'
    },
    {
        id: 'bd7acbea-c1b1-46c2-aedsf5-3ad53sdfabb28ba',
        title: 'First Item',
        pictureDirection: require('../../assets/img/avatar.jpg'),
        name: 'Song 4'
    },
    {
        id: '3ac68afc-c605-48d3-a4f8-fbsdfd91aa97f63',
        title: 'Second Item',
        pictureDirection: require('../../assets/img/HomeBG.png'),
        name: 'Song 5'
    },
    {
        id: '58694a0f-3da1-471f-bd96-145571e2sdf9d72',
        title: 'Third Item',
        pictureDirection: require('../../assets/img/downloadImage.png'),
        name: 'Song 6'
    },
];

function SongsList() {

    return (
        <View>
            <View style={[styles.line]} />
            {
                DATA.map((item) =>
                    <View key={item.id}>
                        <Song showImage={false} name={item.name} />
                        <View style={[styles.line, { width: '100%' }]} />
                    </View>
                )
            }
        </View >

    );
}

export default function AlbumPage(props) {
    const imagePath = '../../assets/img/avatar.jpg'
    return (
        <View style={{ backgroundColor: 'black', flex: 1 }}>
            <ScrollView contentContainerStyle={styles.content}>
                <Image style={styles.image} source={require(imagePath)} />
                <View style={{ width: '80%', marginTop: 10 }}>
                    <Text
                        numberOfLines={1}
                        style={[
                            styles.text,
                            {
                                fontSize: 30,
                                display: 'flex',
                                alignSelf: 'center'
                            }
                        ]}
                    >
                        Album name
                    </Text>
                </View>
                <View style={{ width: '80%', marginBottom: 20, }}>
                    <Text
                        numberOfLines={1}
                        style={[
                            styles.text,
                            {
                                color: '#FF0054',
                                display: 'flex',
                                alignSelf: 'center'
                            }
                        ]}
                    >
                        Album Author
                    </Text>
                </View>

                {/* List of songs */}
                <SongsList />
                <View style={{ width: '100%', paddingHorizontal: 30, display: 'flex', flexDirection: 'row' }}>
                    <Text style={[styles.text, { fontFamily: 'Nunito-Light', color: 'grey', fontSize: '16pt', marginTop: 10, marginBottom: 50 }]}>
                        Number of songs : { }
                    </Text>
                    <Text style={[styles.text, { color: '#FF0054', fontSize: '16pt', marginTop: 10, marginBottom: 50 }]}>
                        {DATA.length}
                    </Text>
                </View>
            </ScrollView>
        </View>
    );
}

const styles = StyleSheet.create({
    content: {
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
    line: {
        borderBottomWidth: 1,
        borderBottomColor: '#5A5A5A',
    },
    image: {
        borderRadius: 10,
        // backgroundColor: "#7cb48f", 
        borderColor: '#5A5A5A',
        borderWidth: 1,
        width: 300,
        height: 300,
    }
})