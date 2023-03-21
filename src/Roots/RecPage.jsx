import React from 'react';
import { StyleSheet, Text, View, ScrollView } from 'react-native';
import Song from '../MusicComponents/SongComponent'

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
                        <Song showImage={true} name={item.name} />
                        <View style={[styles.line, { width: '100%' }]} />
                    </View>
                )
            }
        </View >

    );
}

export default function RecPage({ navigation }) {
    return (
        <View style={{ backgroundColor: 'black', width: '100%', height: '100%' }}>
            <ScrollView contentContainerStyle={styles.container}>
                <Text style={[styles.text, { marginVertical: 25 }]}>Your suggestion list:</Text>
                <SongsList />
            </ScrollView>
        </View>

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
    },
    text: {
        color: 'white',
        fontFamily: 'Nunito-Bold',
        fontSize: '20pt'
    },
    line: {
        borderBottomWidth: 1,
        borderBottomColor: '#5A5A5A',
    },
})