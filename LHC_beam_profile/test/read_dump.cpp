#include <iostream>
#include <string>

#include "H5Cpp.h"

#ifndef H5_NO_NAMESPACE
using namespace H5;
#endif

const H5std_string FN("dump.h5");
const H5std_string DSN_P("/dump/profile_f32");
const H5std_string DSN_TF_REAL("/dump/tf_real_f64");
const H5std_string DSN_TF_IMAG("/dump/tf_imag_f64");

int main (void)
{
	H5File file_p(FN, H5F_ACC_RDWR);
	DataSet ds_p = file_p.openDataSet(DSN_P);
	DataSet ds_tf_real = file_p.openDataSet(DSN_TF_REAL);
	DataSet ds_tf_imag = file_p.openDataSet(DSN_TF_IMAG);

	float buf_p[100][250]; //100 profiles, 250samples each
	ds_p.read(buf_p, PredType::IEEE_F32LE);//NATIVE_FLOAT);//, DataSpace::ALL,DataSpace::ALL,ds_creatplist);
	// p = profile number
	// s = sample number
	for(int32_t p=98; p<99; ++p) {
		for(int32_t s=0; s<50; ++s) {
			std::cout << "[" << s << " of p #" << p << "] = " << buf_p[s][p] << std::endl;
		}
	}

	double buf_tf_real[40000]; //1 trace, 40000 samples 
	float buf_tf_imag[40000]; //1 trace, 40000 samples 
	ds_tf_real.read(buf_tf_real, PredType::IEEE_F64LE);
	ds_tf_imag.read(buf_tf_imag, PredType::IEEE_F32LE);
	for(int32_t i=0; i<10; ++i) {
		std::cout << "[" << i << "] == " << buf_tf_real[i] << " + j* " << buf_tf_imag[i] << std::endl;
	}

}







