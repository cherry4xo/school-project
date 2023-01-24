import React from "react";
import Svg, { Path } from "react-native-svg"


function SearchSVG(props) {
    return (
        <Svg
            width={(props.fill == 'red') ? '40' : '30'}
            height={(props.fill == 'red') ? '40' : '30'}
            viewBox="0 0 30 30"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
        >
            <Path
                fill={props.fill}
                fill-rule="evenodd"
                d="M14.4175 0C22.3673 0 28.8338 6.32381 28.8338 14.0983C28.8338 17.7662 27.3944 21.1116 25.0389 23.6223L29.6737 28.1454C30.1075 28.5696 30.109 29.2559 29.6752 29.68C29.4591 29.8943 29.1734 30 28.8891 30C28.6064 30 28.3221 29.8943 28.1045 29.6829L23.4138 25.1085C20.9462 27.041 17.8175 28.198 14.4175 28.198C6.46772 28.198 -0.000198364 21.8727 -0.000198364 14.0983C-0.000198364 6.32381 6.46772 0 14.4175 0ZM14.4175 2.17164C7.69201 2.17164 2.22042 7.5211 2.22042 14.0983C2.22042 20.6754 7.69201 26.0263 14.4175 26.0263C21.1415 26.0263 26.6131 20.6754 26.6131 14.0983C26.6131 7.5211 21.1415 2.17164 14.4175 2.17164Z"
                clip-rule="evenodd"
            />
        </Svg>

    );
}

export default SearchSVG;