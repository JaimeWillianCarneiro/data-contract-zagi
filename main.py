from datacontract.data_contract import DataContract 



def main():
    contract = DataContract(
        data_contract_file = "datacontract.yaml", 
        server = "ambiente_zagi"
    )

    run  = contract.test()


    if run.has_passed():
        print("Uhuu! Data contract válido :)!!!")
    else:
        print("Ops! Data contract inválido:/!!!")

        for result in run.results:
            print(result)

if __name__ =="__main__":
    main()
    