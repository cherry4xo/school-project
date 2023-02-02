import { Button } from "@react-native-material/core";
import React from "react";
import { StyleSheet, Text, View, TouchableHighlight, Image, ScrollView, Dimensions, } from 'react-native';

const windowWidth = Dimensions.get('window').width;
const windowHeight = Dimensions.get('window').height;

export default function SongComponent(props) {
    return (
        <TouchableHighlight onPress={() => { }}>

            {
                props.showImage ?
                    <View style={styles.content}>
                        <Image style={{ width: 40, height: 35, marginRight: 0, borderRadius: 3 }} source={require('../../assets/img/avatar.jpg')} />
                        <View style={{ width: '60%', fontSize: '18pt', marginHorizontal: 10, display: 'flex', flexDirection: 'column' }}>
                            <Text numberOfLines={1} style={[styles.text, { fontSize: '16pt' }]}>
                                {props.name}
                            </Text>
                            <Text numberOfLines={1} style={[styles.text, { fontSize: '14pt', color: 'grey' }]}>
                                Author
                            </Text>
                        </View>

                        <Text numberOfLines={1} style={[styles.text, { width: '20%', color: '#FF0054', fontFamily: 'Nunito-Bold', fontSize: '16pt' }]}>
                            4:20
                        </Text>
                    </View>
                    :
                    <View style={styles.content}>
                        <Text numberOfLines={1} style={[styles.text, { width: '70%', fontSize: '18pt' }]}>
                            {props.name}
                        </Text>
                        <Text numberOfLines={1} style={[styles.text, { width: '20%', color: '#FF0054', fontFamily: 'Nunito-Bold', fontSize: '16pt' }]}>
                            4:20
                        </Text>
                    </View>
            }

        </TouchableHighlight>
    );
}

const styles = StyleSheet.create({
    content: {
        width: windowWidth - 20,
        display: 'flex',
        flexDirection: 'row',
        height: 45,
        // marginVertical: 10,
        paddingLeft: 30,
        alignItems: 'center',
        justifyContent: 'space-between'
        // borderColor: 'white',
        // borderWidth: 1,
        // borderRadius: 5
    },
    text: {
        color: 'white',
        maxWidth: windowWidth,
        fontFamily: 'Nunito-Medium',
        fontSize: '20pt',
        overflow: 'hidden',
    },
})