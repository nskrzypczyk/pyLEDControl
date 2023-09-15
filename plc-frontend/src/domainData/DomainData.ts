export interface IEffectOptions {
    brightness: number,
    effect: string,
    [name: string]: any
}

export interface IEffectOptionsRawDefinition{
    [name:string]:string
}

type KeyValueMap = {
    [key: string]: new (...args: any[]) => any;
};

export const Python2TsTypeMap:KeyValueMap = {
    "str" : String,
    "int" : Number,
    "float": Number,
    "type" : String,
    "typing.List[str]": Array<string>
}

export const python2TsTypeMapper = (rawType:string) => {
    return Python2TsTypeMap[rawType]
} 

// export const effectDataMapper = (rawData:IEffectOptionsRawDefinition): IEffectOptions => {
//     const returnData: IEffectOptions = {}
//     for (const [k,v] of Object.entries(rawData)){
//         returnData[v]
//     }
//     return returnData
// }