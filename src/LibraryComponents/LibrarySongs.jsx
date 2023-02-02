import React from "react";
import { useEffect } from "react";
import { StyleSheet, Text, View, Image, TouchableHighlight, ScrollView, Dimensions } from 'react-native';

import Song from '../MusicComponents/SongComponent'

const windowWidth = Dimensions.get('window').width;
const windowHeight = Dimensions.get('window').height;

const DATA = [
    {
        id: 'bd7acbea-c1b1-46c32-aed5aa-3ad53abb28ba',
        title: 'First Item',
        pictureDirection: require('../../assets/img/avatar.jpg'),
        name: 'Song 1 lkjfdssdlkfjslkfjdlslkdlkdsjl'
    },
    {
        id: '3ac68afc-c605-48d3-a4f8-6fbd9dfh1aa97f63',
        title: 'Second Item',
        pictureDirection: require('../../assets/img/HomeBG.png'),
        name: 'Song 2'
    },
    {
        id: '58694a0f-3da1-471f-bd96-1asd459571e29d72',
        title: 'Third Item',
        pictureDirection: require('../../assets/img/downloadImage.png'),
        name: 'Song 3'
    },
    {
        id: 'bd7acbea-c1b1-46c2-aeds965f5-3ad53sdfabb28ba',
        title: 'First Item',
        pictureDirection: require('../../assets/img/avatar.jpg'),
        name: 'Song 4'
    },
    {
        id: '3ac68afc456-c605-48d3-a4f8-fbsdfd91aa97f63',
        title: 'Second Item',
        pictureDirection: require('../../assets/img/HomeBG.png'),
        name: 'Song 5'
    },
    {
        id: '58694a0f-3da1-471f-bd7696-145571e2sdf9d72',
        title: 'Third Item',
        pictureDirection: require('../../assets/img/downloadImage.png'),
        name: 'Song 6'
    },
    {
        id: 'bd7acbea-c1b1-4623c2-aed5aa-3ad53abb28ba',
        title: 'First Item',
        pictureDirection: require('../../assets/img/avatar.jpg'),
        name: 'Song 1 lkjfdssdlkfjslkfjdlslkdlkdsjl'
    },
    {
        id: '3ac68afc142-c605-48d3-a4f8-fbd9dfh1aa97f63',
        title: 'Second Item',
        pictureDirection: require('../../assets/img/HomeBG.png'),
        name: 'Song 2'
    },
    {
        id: '58694a0f-3da1-47121f-bd96-1asd45571e29d72',
        title: 'Third Item',
        pictureDirection: require('../../assets/img/downloadImage.png'),
        name: 'Song 3'
    },
    {
        id: 'bd7acbea-c1b1-46c2-aed642sf5-3ad53sdfabb28ba',
        title: 'First Item',
        pictureDirection: require('../../assets/img/avatar.jpg'),
        name: 'Song 4'
    },
    {
        id: '3ac68afc-c605-48d3-325264a4f8-fbsdfd91aa97f63',
        title: 'Second Item',
        pictureDirection: require('../../assets/img/HomeBG.png'),
        name: 'Song 5'
    },
    {
        id: '58694a0f-3da1-471f-b3523d96-145571e2sdf9d72',
        title: 'Third Item',
        pictureDirection: require('../../assets/img/downloadImage.png'),
        name: 'Song 6'
    },
    {
        id: 'bd7acbea-c1b1-46c2-aed51231aa-3ad53abb28ba',
        title: 'First Item',
        pictureDirection: require('../../assets/img/avatar.jpg'),
        name: 'Song 1 lkjfdssdlkfjslkfjdlslkdlkdsjl'
    },
    {
        id: '3ac68afc-c605-48d3-a3454f8-fbd9dfh1aa97f63',
        title: 'Second Item',
        pictureDirection: require('../../assets/img/HomeBG.png'),
        name: 'Song 2'
    },
    {
        id: '58694a0f-3da1-471f-bd96-1asd45571234e29d72',
        title: 'Third Item',
        pictureDirection: require('../../assets/img/downloadImage.png'),
        name: 'Song 3'
    },
    {
        id: 'bd7acbea-c1b1-46c2-aedsf5-3ad53sdfabb2238ba',
        title: 'First Item',
        pictureDirection: require('../../assets/img/avatar.jpg'),
        name: 'Song 4'
    },
    {
        id: '3131ac68afc-c605-48d3-a4f8-fbsdfd91aa97f63',
        title: 'Second Item',
        pictureDirection: require('../../assets/img/HomeBG.png'),
        name: 'Song 5'
    },
    {
        id: '58694a0f-3132da1-471f-bd96-145571e2sdf9d72',
        title: 'Third Item',
        pictureDirection: require('../../assets/img/downloadImage.png'),
        name: 'Song 6'
    },
    {
        id: 'bd7acbea-c1b1-46c2-ae123d5aa-3ad53abb28ba',
        title: 'First Item',
        pictureDirection: require('../../assets/img/avatar.jpg'),
        name: 'Song 1 lkjfdssdlkfjslkfjdlslkdlkdsjl'
    },
    {
        id: '3ac68afc-c605-48asdd3-a4f8-fbd9dfh1aa97f63',
        title: 'Second Item',
        pictureDirection: require('../../assets/img/HomeBG.png'),
        name: 'Song 2'
    },
    {
        id: '58694a0f-3da1-47dfs1f-bd96-1asd45571e29d72',
        title: 'Third Item',
        pictureDirection: require('../../assets/img/downloadImage.png'),
        name: 'Song 3'
    },
    {
        id: 'bd7acbea-c1b1-46c2-aeds    asf5-3ad53sdfabb28ba',
        title: 'First Item',
        pictureDirection: require('../../assets/img/avatar.jpg'),
        name: 'Song 4'
    },
    {
        id: '3ac68afc-c605-48d3-a4f8qr-fbsdfd91aa97f63',
        title: 'Second Item',
        pictureDirection: require('../../assets/img/HomeBG.png'),
        name: 'Song 5'
    },
    {
        id: '58694a0f-3da1-471f-bd96e-145571e2sdf9d72',
        title: 'Third Item',
        pictureDirection: require('../../assets/img/downloadImage.png'),
        name: 'Song 6'
    },
    {
        id: 'bd7acbea-c1b1-46c2-aedwte5aa-3ad53abb28ba',
        title: 'First Item',
        pictureDirection: require('../../assets/img/avatar.jpg'),
        name: 'Song 1 lkjfdssdlkfjslkfjdlslkdlkdsjl'
    },
    {
        id: '3ac68afc-c605-48d3-a4f8-fbdqwr9dfh1aa97f63',
        title: 'Second Item',
        pictureDirection: require('../../assets/img/HomeBG.png'),
        name: 'Song 2'
    },
    {
        id: '58694a0f-3da1-471f-bd96-1asd4557hfdg1e29d72',
        title: 'Third Item',
        pictureDirection: require('../../assets/img/downloadImage.png'),
        name: 'Song 3'
    },
    {
        id: 'bd7acbea-c1b1-46c2-aedsf5sdg-3ad53sdfabb28ba',
        title: 'First Item',
        pictureDirection: require('../../assets/img/avatar.jpg'),
        name: 'Song 4'
    },
    {
        id: '3ac68afc-c605-48d3-a4f8asf-fbsdfd91aa97f63',
        title: 'Second Item',
        pictureDirection: require('../../assets/img/HomeBG.png'),
        name: 'Song 5'
    },
    {
        id: '58694a0f-3da1-471f-bd96-1a45571e2sdf9d72',
        title: 'Third Item',
        pictureDirection: require('../../assets/img/downloadImage.png'),
        name: 'Song 6'
    },
    {
        id: 'bd7acbea-c1b1-46c2-aed5aas-3ad53abb28ba',
        title: 'First Item',
        pictureDirection: require('../../assets/img/avatar.jpg'),
        name: 'Song 1 lkjfdssdlkfjslkfjdlslkdlkdsjl'
    },
    {
        id: '3ac68afc-c605-48d3-a4f8-fgbd9dfh1aa97f63',
        title: 'Second Item',
        pictureDirection: require('../../assets/img/HomeBG.png'),
        name: 'Song 2'
    },
    {
        id: '58694a0f-3da1-471af-bd96-1asd45571e29d72',
        title: 'Third Item',
        pictureDirection: require('../../assets/img/downloadImage.png'),
        name: 'Song 3'
    },
    {
        id: 'bd7acbsea-c1b1-46c2-aedsf5-3ad53sdfabb28ba',
        title: 'First Item',
        pictureDirection: require('../../assets/img/avatar.jpg'),
        name: 'Song 4'
    },
    {
        id: '3ac68afc-c605-48dd3-a4f8-fbsdfd91aa97f63',
        title: 'Second Item',
        pictureDirection: require('../../assets/img/HomeBG.png'),
        name: 'Song 5'
    },
    {
        id: '58694a0f-3da1-471f-bd96-1455d71e2sdf9d72',
        title: 'Third Item',
        pictureDirection: require('../../assets/img/downloadImage.png'),
        name: 'Song 6'
    },
    {
        id: 'bd7acbea-c1b1-46c2dfg-aed5aa-3ad53abb28ba',
        title: 'First Item',
        pictureDirection: require('../../assets/img/avatar.jpg'),
        name: 'Song 1 lkjfdssdlkfjslkfjdlslkdlkdsjl'
    },
    {
        id: '3ac68afcad-c605-48d3-a4f8-fbd9dfh1aa97f63',
        title: 'Second Item',
        pictureDirection: require('../../assets/img/HomeBG.png'),
        name: 'Song 2'
    },
    {
        id: '58694a0f-3da1-471dsff-bd96-1asd45571e29d72',
        title: 'Third Item',
        pictureDirection: require('../../assets/img/downloadImage.png'),
        name: 'Song 3'
    },
    {
        id: 'bd7acbea-c1b1-46c2-aedsf5-3dsaad53sdfabb28ba',
        title: 'First Item',
        pictureDirection: require('../../assets/img/avatar.jpg'),
        name: 'Song 4'
    },
    {
        id: '3ac68afc-c605-48d3-a4f8-fbsdfda91aa97f63',
        title: 'Second Item',
        pictureDirection: require('../../assets/img/HomeBG.png'),
        name: 'Song 5'
    },
    {
        id: '58694a0f-3da1-471f-bd96-1sdf45571e2sdf9d72',
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

export default function LibrarySongs(props) {
    return (
        <View style={{ backgroundColor: 'black', flex: 1 }}>
            <ScrollView contentContainerStyle={styles.content}>
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