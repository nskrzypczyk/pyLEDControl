type TEffectOptionsOutput = {
    [key: string]: any;
}

export interface IEffectOptionsDefinition {
    [name: string]: IEffectPropertyDefinition
}

export interface IEffectPropertyDefinition{
    type:string,
    dataComponent?:IDataComponent
}

type TIntervalDataComponentDefBounds = {
    inclusive: boolean
    value: number
}

export interface IIntervalDataComponent{
    lower_bound:TIntervalDataComponentDefBounds,
    upper_bound:TIntervalDataComponentDefBounds
}

export interface IDataComponent{
    type:string 
}

export interface IStatus extends Record<string, any> {
    effect:string,
    brightness: number
    [key: string]: any;
}

export type TimerDataComponent = {
    start: string,
    end: string,
    selectedDays: string[],
    enabled: boolean
}

/*-------------------------------------*/

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
